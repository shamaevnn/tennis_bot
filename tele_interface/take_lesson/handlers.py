import calendar
from datetime import datetime

from admin_bot.keyboard_utils import yes_no_permission4ind_train_keyboard
from admin_bot.static_text import GROUP_LEVEL_DICT, DATE_INFO
from base.models import User, TrainingGroup, GroupTrainingDay
from base.utils import bot_edit_message, moscow_datetime, DT_BOT_FORMAT, clear_broadcast_messages, \
    get_time_info_from_tr_day, get_actual_players_without_absent
from tele_interface.keyboard_utils import ind_group_type_training_keyboard, create_calendar, \
    ind_train_choose_duration_keyboard, take_lesson_back_keyboard, choose_type_of_payment_for_group_lesson_keyboard, \
    back_to_group_times_when_no_left_keyboard
from tele_interface.manage_data import SELECT_TRAINING_TYPE, CLNDR_ACTION_TAKE_GROUP, SELECT_DURATION_FOR_IND_TRAIN, \
    CLNDR_ACTION_TAKE_IND, SELECT_PRECISE_IND_TIME, SELECT_PRECISE_GROUP_TIME, CONFIRM_GROUP_LESSON, PAYMENT_VISITING, \
    PAYMENT_BONUS, PAYMENT_MONEY
from tele_interface.static_text import from_eng_to_rus_day_week
from tele_interface.take_lesson.utils import get_potential_days_for_group_training
from tele_interface.utils import check_status_decor
from tennis_bot.settings import ADMIN_TELEGRAM_TOKEN, TARIF_ARBITRARY, TARIF_GROUP, TARIF_PAYMENT_ADD_LESSON


@check_status_decor
def choose_type_of_training(update, context):
    markup = ind_group_type_training_keyboard()
    text = 'Выбери тип тренировки.'
    if update.callback_query:
        bot_edit_message(context.bot, text, update, markup)
    else:
        update.message.reply_text(
            text=text,
            reply_markup=markup
        )


@check_status_decor
def take_lesson(update, context):
    """записаться на тренировку"""
    user, _ = User.get_user_and_created(update, context)
    tr_type = update.callback_query.data[len(SELECT_TRAINING_TYPE):]
    if tr_type == 'group':
        if user.bonus_lesson > 0:
            text = 'Выбери тренировку для записи.\n' \
                   '<b>Пожертвуешь одним отыгрышем.</b>\n' \
                   '✅ -- дни, доступные для групповых тренировок.'
        else:
            text = '⚠️ATTENTION⚠️\n' \
                   'В данный момент у тебя нет отыгрышей.\n' \
                   '<b> Занятие будет стоить 600₽ </b>\n' \
                   '✅ -- дни, доступные для групповых тренировок.'
        training_days = get_potential_days_for_group_training(user).filter(
            date__gte=moscow_datetime(datetime.now()).date())
        highlight_dates = list(training_days.values_list('date', flat=True))
        markup = create_calendar(CLNDR_ACTION_TAKE_GROUP, dates_to_highlight=highlight_dates)

    else:
        markup = ind_train_choose_duration_keyboard()
        text = 'Выбери продолжительность занятия'

    bot_edit_message(context.bot, text, update, markup)


def select_dt_for_ind_lesson(update, context):
    duration = float(update.callback_query.data[len(SELECT_DURATION_FOR_IND_TRAIN):])
    markup = create_calendar(f'{CLNDR_ACTION_TAKE_IND}{duration}')
    text = 'Выбери дату тренировки.'
    bot_edit_message(context.bot, text, update, markup)


def select_precise_ind_lesson_time(update, context):
    day_dt, start_time, end_time = update.callback_query.data[len(SELECT_PRECISE_IND_TIME):].split('|')
    date_dt = datetime.strptime(day_dt, DT_BOT_FORMAT)
    st_time_obj = datetime.strptime(start_time, '%H:%M:%S')
    end_time_obj = datetime.strptime(end_time, '%H:%M:%S')
    duration = end_time_obj - st_time_obj

    day_of_week = from_eng_to_rus_day_week[calendar.day_name[date_dt.date().weekday()]]

    user, _ = User.get_user_and_created(update, context)
    group, _ = TrainingGroup.objects.get_or_create(name=user.first_name + user.last_name,
                                                   max_players=1)

    tr_day = GroupTrainingDay.objects.create(group=group, date=date_dt, start_time=st_time_obj, duration=duration,
                                             is_individual=True)

    text = f"Сообщу тренеру, что ты хочешь прийти на индивидуальное занятие"\
           f" <b>{day_dt} ({day_of_week}) </b>\n"\
           f"Время: <b>{start_time} — {end_time}</b>"
    bot_edit_message(context.bot, text, update)

    admins = User.objects.filter(is_staff=True, is_blocked=False)
    markup = yes_no_permission4ind_train_keyboard(
        user_id=user.id,
        tr_day_id=tr_day.id,
    )

    text = f"<b>{user.first_name} {user.last_name} — {user.phone_number}</b>\n" \
           f"Хочет прийти на индивидуальное занятие <b>{day_dt} ({day_of_week}) </b>" \
           f" в <b>{start_time} — {end_time}</b>\n" \
           f"<b>Разрешить?</b>"

    clear_broadcast_messages(
        user_ids=list(admins.values_list('id', flat=True)),
        message=text,
        reply_markup=markup,
        tg_token=ADMIN_TELEGRAM_TOKEN
    )


def select_precise_group_lesson_time(update, context):
    """
    после того, как выбрал точное время для групповой тренировки,
    показываем инфу об этом дне с кнопкой записаться и назад
    :param bot:
    :param update:
    :param user:
    :return:
    """

    tr_day_id = update.callback_query.data[len(SELECT_PRECISE_GROUP_TIME):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    # сколько сейчас свободных мест
    players = get_actual_players_without_absent(tr_day)
    n_free_places = tr_day.group.max_players - players.count()
    all_players = players.values('first_name', 'last_name')
    text = ''
    if n_free_places <= 0 and tr_day.group.max_players < 6 and tr_day.group.available_for_additional_lessons:
        text = f'⚠️ATTENTION⚠️\n' \
               f'<b>Это занятие платное!</b>\n\n'

    all_players = '\n'.join((f"{x['first_name']} {x['last_name']}" for x in all_players))
    text += f'{tr_day.group.name} -- {GROUP_LEVEL_DICT[tr_day.group.level]}\n' \
            f'{DATE_INFO.format(date_tlg, day_of_week, time_tlg)}' \
            f'👥Присутствующие:\n{all_players}\n\n' \
            f'Свободные места: {n_free_places if n_free_places > 0 else "есть за деньги"}'

    markup = take_lesson_back_keyboard(
        tr_day_id=tr_day_id,
        year=tr_day.date.year,
        month=tr_day.date.month,
        day=tr_day.date.day,
    )

    bot_edit_message(context.bot, text, update, markup)


def confirm_group_lesson(update, context):
    tr_day_id = update.callback_query.data[len(CONFIRM_GROUP_LESSON):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)
    user, _ = User.get_user_and_created(update, context)

    time_tlg, start_time_tlg, end_time_tlg, date_tlg, day_of_week, start_time, end_time = get_time_info_from_tr_day(
        tr_day)
    n_free_places = tr_day.group.max_players - tr_day.visitors.distinct().count() + \
                    tr_day.absent.distinct().count() - tr_day.group.users.distinct().count()
    admit_message_text = ''

    if n_free_places > 0:
        tr_day.visitors.add(user)
        text = f'Записал тебя на тренировку.\n' \
               f'{DATE_INFO.format(date_tlg, day_of_week, time_tlg)}'
        markup = None

        if user.bonus_lesson > 0 and user.status == User.STATUS_TRAINING:
            admit_message_text = f'{user.first_name} {user.last_name} записался на групповую тренировку за отыгрыш.\n' \
                                 f'{DATE_INFO.format(date_tlg, day_of_week, time_tlg)}'
            user.bonus_lesson -= 1
            user.save()
        else:
            admit_message_text = f'⚠️ATTENTION⚠️\n' \
                                 f'{user.first_name} {user.last_name} записался на <b>{date_tlg} ({day_of_week})</b>\n' \
                                 f'Время: <b>{time_tlg}</b>\n' \
                                 f'<b>Не за счет отыгрышей, не забудь взять с него денюжку.</b>'
    else:
        if tr_day.group.available_for_additional_lessons and tr_day.group.max_players < 6:
            tarif = TARIF_ARBITRARY if user.status == User.STATUS_ARBITRARY else TARIF_GROUP
            if user.bonus_lesson == 0:
                tr_day.pay_visitors.add(user)
                text = f'Записал тебя на <b>{date_tlg} ({day_of_week})</b>\n' \
                       f'Время: <b>{time_tlg}</b>\n' \
                       f'⚠️ATTENTION⚠️\n' \
                       f'Не забудь заплатить <b>{tarif}₽</b>'
                admit_message_text = f'⚠️ATTENTION⚠️\n' \
                                     f'{user.first_name} {user.last_name} записался на <b>{date_tlg} ({day_of_week})</b>\n' \
                                     f'Время: <b>{time_tlg}</b>\n' \
                                     f'<b>Не за счет отыгрышей, не забудь взять с него {tarif}₽.</b>'
                markup = None
            else:
                text = "Выбери тип оплаты"
                markup = choose_type_of_payment_for_group_lesson_keyboard(
                    payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                    tr_day_id=tr_day_id,
                    tarif=tarif,
                )
        else:
            text = 'Упс, похоже уже не осталось свободных мест на это время, выбери другое.'
            markup = back_to_group_times_when_no_left_keyboard(
                year=tr_day.date.year,
                month=tr_day.date.month,
                day=tr_day.date.day
            )

    bot_edit_message(context.bot, text, update, markup)

    if admit_message_text:
        admins = User.objects.filter(is_staff=True, is_blocked=False)

        clear_broadcast_messages(
            user_ids=list(admins.values_list('id', flat=True)),
            message=admit_message_text,
            reply_markup=None,
            tg_token=ADMIN_TELEGRAM_TOKEN
        )


def choose_type_of_payment_for_pay_visiting(update, context):
    payment_choice, tr_day_id = update.callback_query.data[len(PAYMENT_VISITING):].split('|')
    tr_day = GroupTrainingDay.objects.get(id=tr_day_id)
    user, _ = User.get_user_and_created(update, context)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    text, admin_text = '', ''
    if payment_choice == PAYMENT_BONUS:
        user.bonus_lesson -= 1
        user.save()

        tr_day.pay_bonus_visitors.add(user)
        text = f'Записал тебя на <b>{date_tlg} ({day_of_week})</b>\n' \
               f'Время: <b>{time_tlg}</b>\n' \
               f'⚠️ATTENTION⚠️\n' \
               f'Не забудь заплатить <b>{TARIF_PAYMENT_ADD_LESSON}₽</b>'

        admin_text = f'⚠️ATTENTION⚠️\n' \
                     f'{user.first_name} {user.last_name} записался на <b>{date_tlg} ({day_of_week})</b>\n' \
                     f'Время: <b>{time_tlg}</b>\n' \
                     f'<b>За счет платных отыгрешей, не забудь взять с него {TARIF_PAYMENT_ADD_LESSON}₽.</b>'

    elif payment_choice == PAYMENT_MONEY:
        tr_day.pay_visitors.add(user)
        tarif = TARIF_ARBITRARY if user.status == User.STATUS_ARBITRARY else TARIF_GROUP

        text = f'Записал тебя на <b>{date_tlg} ({day_of_week})</b>\n' \
               f'Время: <b>{time_tlg}</b>\n' \
               f'⚠️ATTENTION⚠️\n' \
               f'Не забудь заплатить <b>{tarif}₽</b>'

        admin_text = f'⚠️ATTENTION⚠️\n' \
                     f'{user.first_name} {user.last_name} записался на <b>{date_tlg} ({day_of_week})</b>\n' \
                     f'Время: <b>{time_tlg}</b>\n' \
                     f'<b>В дополнительное время, не забудь взять с него {tarif}₽.</b>'

    bot_edit_message(context.bot, text, update)

    admins = User.objects.filter(is_staff=True, is_blocked=False)

    clear_broadcast_messages(
        user_ids=list(admins.values_list('id', flat=True)),
        message=admin_text,
        reply_markup=None,
        tg_token=ADMIN_TELEGRAM_TOKEN
    )
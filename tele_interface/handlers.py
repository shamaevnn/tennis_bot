import re

from telegram.ext import ConversationHandler

from admin_bot.keyboard_utils import yes_no_permission4ind_train_keyboard, go_to_site_set_up_personal_data
from admin_bot.static_text import NEW_CLIENT_HAS_COME, GROUP_LEVEL_DICT, DATE_INFO
from tennis_bot.settings import TARIF_ARBITRARY, TARIF_GROUP, TARIF_PAYMENT_ADD_LESSON
from .utils import *
from .keyboard_utils import *
from base.utils import (DT_BOT_FORMAT, moscow_datetime, bot_edit_message,
                        get_time_info_from_tr_day, info_about_users, clear_broadcast_messages, construct_main_menu,
                        get_actual_players_without_absent,
                        )
from base.models import (User,
                         GroupTrainingDay,
                         TrainingGroup,
                         Payment)
from .manage_data import *
from .static_text import *
from calendar import monthrange
from tennis_bot.settings import ADMIN_TELEGRAM_TOKEN
from datetime import date, datetime, timedelta
from django.db.models import Q


INSERT_FIO, INSERT_PHONE_NUMBER = range(2)


def get_first_last_name(update, context):
    user, _ = User.get_user_and_created(update, context)
    text = update.message.text

    last_name, first_name = text.split(' ')
    user.last_name = last_name
    user.first_name = first_name
    user.save()

    update.message.reply_text(
        text=FIRST_TIME_INSERT_PHONE_NUMBER,
    )
    return INSERT_PHONE_NUMBER


def get_phone_number(update, context):
    user, _ = User.get_user_and_created(update, context)
    text = update.message.text
    phone_number_candidate = re.findall(r'\d+', text)

    if len(phone_number_candidate[0]) != 11:
        update.message.reply_text(
            text=WRONG_PHONE_NUMBER_FORMAT.format(len(phone_number_candidate[0])),
        )
        return INSERT_PHONE_NUMBER
    else:
        user.phone_number = int(phone_number_candidate[0])
        user.save()

        update.message.reply_text(
            text=I_WILL_TEXT_AS_SOON_AS_COACH_CONFIRM,
            reply_markup=construct_main_menu()
        )

        admins = User.objects.filter(is_staff=True)

        clear_broadcast_messages(
            user_ids=list(admins.values_list('id', flat=True)),
            message=NEW_CLIENT_HAS_COME.format(user),
            reply_markup=go_to_site_set_up_personal_data(user.id),
            tg_token=ADMIN_TELEGRAM_TOKEN,
        )

    return ConversationHandler.END


def get_help(update, context):
    user, _ = User.get_user_and_created(update, context)
    update.message.reply_text(text=HELP_MESSAGE,
                              reply_markup=construct_main_menu(user, user.status))


@check_status_decor
def user_main_info(update, context):
    """посмотреть, основную инфу:
        статус
        группа, если есть
        отыгрыши
        сколько должен заплатить
    """

    from_user_to_intro = {
        User.STATUS_WAITING: 'в листе ожидания.',
        User.STATUS_TRAINING: 'тренируешься в группе.',
        User.STATUS_FINISHED: 'закончил тренировки.',
        User.STATUS_ARBITRARY: 'тренируешься по свободному графику.'
    }

    today_date = date.today()
    user, _ = User.get_user_and_created(update, context)
    user_payment = Payment.objects.filter(player=user, player__status=User.STATUS_TRAINING, fact_amount=0,
                                          year=today_date.year - 2020, month=today_date.month)

    if user.status == User.STATUS_TRAINING:
        if user_payment.exists():
            payment_status = f'{NO_PAYMENT_BUTTON}\n'
        else:
            payment_status = f'{SUCCESS_PAYMENT}\n'
    else:
        payment_status = ''

    intro = f'В данный момент ты {from_user_to_intro[user.status]}\n\n'

    group = TrainingGroup.objects.filter(users__in=[user]).exclude(max_players=1).first()

    teammates = group.users.values('first_name', 'last_name') if group else []

    group_info = "Твоя группа -- {}:\n{}\n\n".format(group.name, info_about_users(teammates)) if teammates else ''

    number_of_add_games = 'Количество отыгрышей: <b>{}</b>\n\n'.format(user.bonus_lesson)

    today = moscow_datetime(datetime.now()).date()
    number_of_days_in_month = monthrange(today.year, today.month)[1]
    last_day = date(today.year, today.month, number_of_days_in_month)
    next_month = last_day + timedelta(days=1)

    should_pay_this_month, balls_this_month, _ = balls_lessons_payment(today.year, today.month, user)
    should_pay_money_next, balls_next_month, _ = balls_lessons_payment(next_month.year, next_month.month, user)

    should_pay_info = 'В этом месяце ({}) <b>нужно заплатить {} ₽ + {} ₽ за мячи.</b>\n' \
                      'В следующем месяце ({}) <b>нужно заплатить {} ₽ + {} ₽ за мячи</b>.'.format(
        from_digit_to_month[today.month], should_pay_this_month, balls_this_month,
        from_digit_to_month[next_month.month], should_pay_money_next, balls_next_month)

    text = intro + group_info + number_of_add_games + payment_status + should_pay_info

    update.message.reply_text(
        text=text,
        parse_mode='HTML',
        reply_markup=construct_main_menu(user, user.status)
    )
    return ConversationHandler.END


def process_calendar_selection(update, context):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    """
    user, _ = User.get_user_and_created(update, context)

    query = update.callback_query
    (purpose, action, year, month, day) = separate_callback_data(query.data)
    curr = datetime(int(year), int(month), 1)

    if purpose == CLNDR_ACTION_SKIP:
        highlight_dates = list(select_tr_days_for_skipping(user).values_list('date', flat=True))
    elif purpose == CLNDR_ACTION_TAKE_GROUP:
        training_days = get_potential_days_for_group_training(user)
        highlight_dates = list(training_days.values_list('date', flat=True))
    elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
        highlight_dates = None

    if action == CLNDR_IGNORE:
        context.bot.answer_callback_query(callback_query_id=query.id)
    # elif action == CLNDR_CHANGE_FREE_OR_FOR_MONEY:
    #     pass
    elif action == CLNDR_DAY:
        bot_edit_message(context.bot, query.message.text, update)
        return True, purpose, datetime(int(year), int(month), int(day))
    elif action == CLNDR_PREV_MONTH:
        pre = curr - timedelta(days=1)
        bot_edit_message(context.bot, query.message.text, update, create_calendar(purpose, int(pre.year), int(pre.month),
                                                                          highlight_dates))
    elif action == CLNDR_NEXT_MONTH:
        ne = curr + timedelta(days=31)
        bot_edit_message(context.bot, query.message.text, update, create_calendar(purpose, int(ne.year), int(ne.month),
                                                                          highlight_dates))
    elif action == CLNDR_ACTION_BACK:
        if purpose == CLNDR_ACTION_SKIP:
            text = 'Выбери дату тренировки для отмены.\n' \
                   '✅ -- дни, доступные для отмены.'
        elif purpose == CLNDR_ACTION_TAKE_GROUP:
            text = 'Выбери дату тренировки\n' \
                   '✅ -- дни, доступные для групповых тренировок'
        elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
            text = 'Выбери дату индивидуальной тренировки'
        bot_edit_message(context.bot, text, update, create_calendar(purpose, int(year), int(month), highlight_dates))

    else:
        context.bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    return False, purpose, []


@check_status_decor
def inline_calendar_handler(update, context):
    user, _ = User.get_user_and_created(update, context)

    selected, purpose, date_my = process_calendar_selection(update, context)
    today_date = moscow_datetime(datetime.now()).date()
    if selected:
        date_comparison = date(date_my.year, date_my.month, date_my.day)
        if purpose == CLNDR_ACTION_SKIP:
            if date_comparison < today_date:
                text = 'Тренировка уже прошла, ее нельзя отменить.\n' \
                       '✅ -- дни, доступные для отмены.'
                markup = create_calendar(CLNDR_ACTION_SKIP, date_my.year, date_my.month,
                                         list(select_tr_days_for_skipping(user).values_list('date', flat=True)))
            else:
                training_days = GroupTrainingDay.objects.filter(
                    Q(group__users__in=[user]) |
                    Q(visitors__in=[user]) |
                    Q(pay_visitors__in=[user]) |
                    Q(pay_bonus_visitors__in=[user]),
                    date=date_my
                ).exclude(absent__in=[user]).select_related('group').order_by('id').distinct('id')
                if training_days.exists():
                    if training_days.count() > 1:
                        markup = construct_menu_skipping_much_lesson(training_days)
                        text = 'Выбери время'
                    else:
                        training_day = training_days.first()
                        group_name, group_players = make_group_name_group_players_info_for_skipping(training_day)

                        markup, text = construct_detail_menu_for_skipping(training_day, purpose, group_name,
                                                                          group_players)

                else:
                    text = 'Нет тренировки в этот день, выбери другой.\n' \
                           '✅ -- дни, доступные для отмены.'
                    markup = create_calendar(purpose, date_my.year, date_my.month,
                                             list(select_tr_days_for_skipping(user).values_list('date', flat=True)))

        elif purpose == CLNDR_ACTION_TAKE_GROUP:
            training_days = get_potential_days_for_group_training(user)
            highlight_dates = list(training_days.values_list('date', flat=True))
            if date_comparison < today_date:
                text = 'Тренировка уже прошла, на нее нельзя записаться.\n' \
                       '✅ -- дни, доступные для групповых тренировок'
                markup = create_calendar(purpose, date_my.year, date_my.month, highlight_dates)
            else:
                training_days = training_days.filter(date=date_comparison)
                if training_days.exists():
                    buttons = construct_time_menu_for_group_lesson(SELECT_PRECISE_GROUP_TIME, training_days, date_my,
                                                                   purpose)

                    day_of_week = calendar.day_name[date_my.weekday()]
                    text = f'Выбери время занятия на {date_my.strftime(DT_BOT_FORMAT)} ({from_eng_to_rus_day_week[day_of_week]}).'
                    markup = buttons

                else:
                    text = 'Нет доступных тренировок в этот день, выбери другой.\n' \
                           '✅ -- дни, доступные для групповых тренировок'
                    markup = create_calendar(purpose, date_my.year, date_my.month, highlight_dates)

        elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
            duration = re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose)[0][1]
            date_time_dict = get_available_dt_time4ind_train(float(duration), date_comparison)
            if date_comparison < today_date:
                text = 'Это уже в прошлом, давай не будем об этом.'
                markup = create_calendar(f'{CLNDR_ACTION_TAKE_IND}{duration}', date_my.year, date_my.month)
            else:
                poss_time_for_train = []
                if date_time_dict.get(date_comparison):
                    for i in range(len(date_time_dict[date_comparison]) - int(float(duration) * 2)):
                        if datetime.combine(date_comparison, date_time_dict[date_comparison][
                                                i + int(float(duration) * 2)]) - datetime.combine(
                             date_comparison, date_time_dict[date_comparison][i]) == timedelta(hours=float(duration)):
                            poss_time_for_train.append(date_time_dict[date_comparison][i])

                    markup = construct_time_menu_4ind_lesson(SELECT_PRECISE_IND_TIME, poss_time_for_train,
                                                             date_comparison,
                                                             float(duration), user)
                    text = 'Выбери время'
                else:
                    text = 'Нельзя записаться на этот день, выбери другой.'
                    markup = create_calendar(purpose, date_my.year, date_my.month)

        bot_edit_message(context.bot, text, update, markup)


@check_status_decor
def skip_lesson_main_menu_button(update, context):
    user, _ = User.get_user_and_created(update, context)
    available_grouptraining_dates = select_tr_days_for_skipping(user)
    if available_grouptraining_dates.exists():
        context.bot.send_message(
            user.id,
            'Выбери дату тренировки для отмены.\n'
            '✅ -- дни, доступные для отмены.',
            reply_markup=create_calendar(CLNDR_ACTION_SKIP,
                                         dates_to_highlight=list(
                                             available_grouptraining_dates.values_list('date', flat=True))
                                         )
        )
    else:
        context.bot.send_message(
            user.id,
            'Пока что нечего пропускать.',
            reply_markup=construct_main_menu(user, user.status)
        )


@check_status_decor
def skip_lesson_when_geq_2(update, context):
    tr_day_id = update.callback_query.data[len(SELECT_SKIP_TIME_BUTTON):]
    training_day = GroupTrainingDay.objects.get(id=tr_day_id)

    group_name, group_players = make_group_name_group_players_info_for_skipping(training_day)
    markup, text = construct_detail_menu_for_skipping(training_day, CLNDR_ACTION_SKIP, group_name, group_players)
    bot_edit_message(context.bot, text, update, markup)


@check_status_decor
def skip_lesson(update, context):
    user, _ = User.get_user_and_created(update, context)

    tr_day_id = update.callback_query.data[len(SHOW_INFO_ABOUT_SKIPPING_DAY):]
    training_day = GroupTrainingDay.objects.get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(training_day)

    admins = User.objects.filter(is_superuser=True, is_blocked=False)
    if not training_day.is_available:
        text = "{} в {} ❌нет тренировки❌, т.к. она отменена тренером, поэтому ее нельзя пропустить.".format(date_tlg, time_tlg)
        bot_edit_message(context.bot, text, update)

        skip_lesson_main_menu_button(context.bot, update)

    else:
        if datetime.combine(training_day.date, training_day.start_time) - moscow_datetime(datetime.now()) < user.time_before_cancel:
            text = f'Неа, уже нельзя отменить занятие.' \
                   f' Количество часов, за которое тебе нужно отменять: {round(user.time_before_cancel.seconds/3600)}'
        else:
            text = 'Окей, занятие <b>{}</b> в <b>{}</b> отменено'.format(date_tlg, time_tlg)

            if training_day.is_individual:
                training_day.delete()

                admin_text = f'⚠️ATTENTION⚠️\n' \
                             f'{user.first_name} {user.last_name} отменил индивидуальную тренировку\n' \
                             f'{DATE_INFO.format(date_tlg, day_of_week, time_tlg)}'
            else:
                # проверяем его ли эта группа или он удаляется из занятия другой группы
                if user in training_day.visitors.all():
                    user.bonus_lesson += 1
                    training_day.visitors.remove(user)
                    admin_text = f'{user.first_name} {user.last_name} пропускает тренировку за <b>отыгрыш</b>\n' \
                                 f'{DATE_INFO.format(date_tlg, day_of_week, time_tlg)}'
                elif user in training_day.pay_visitors.all():
                    # в этом случае не должно поменяться кол-во отыгрышей
                    training_day.pay_visitors.remove(user)
                    admin_text = f'{user.first_name} {user.last_name} пропускает тренировку за <b>оплату</b>\n' \
                                 f'{DATE_INFO.format(date_tlg, day_of_week, time_tlg)}'
                elif user in training_day.pay_bonus_visitors.all():
                    user.bonus_lesson += 1
                    training_day.pay_bonus_visitors.remove(user)
                    admin_text = f'{user.first_name} {user.last_name} пропускает тренировку за <b>платный отыгрыш</b>\n' \
                                 f'{DATE_INFO.format(date_tlg, day_of_week, time_tlg)}'
                else:
                    user.bonus_lesson += 1
                    training_day.absent.add(user)
                    admin_text = f'{user.first_name} {user.last_name} пропускает тренировку в <b>своей группе</b>\n' \
                                 f'{DATE_INFO.format(date_tlg, day_of_week, time_tlg)}'
                user.save()

            clear_broadcast_messages(
                user_ids=list(admins.values_list('id', flat=True)),
                message=admin_text,
                tg_token=ADMIN_TELEGRAM_TOKEN,
            )

        bot_edit_message(context.bot, text, update)


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

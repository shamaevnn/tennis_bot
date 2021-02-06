from admin_bot.handlers import info_about_users
from .utils import (handler_decor,
                    get_available_dt_time4ind_train, select_tr_days_for_skipping,
                    get_potential_days_for_group_training, separate_callback_data, create_callback_data,
                    create_calendar, construct_time_menu_for_group_lesson, construct_detail_menu_for_skipping,
                    construct_time_menu_4ind_lesson, construct_menu_skipping_much_lesson, balls_lessons_payment,
                    )
from base.utils import (send_message, DT_BOT_FORMAT, moscow_datetime, bot_edit_message,
                        get_time_info_from_tr_day, construct_main_menu,
                        )
from base.models import (User,
                         GroupTrainingDay,
                         TrainingGroup,
                         StaticData,
                         Payment)
from .manage_data import (
    SELECT_PRECISE_GROUP_TIME,
    from_eng_to_rus_day_week,
    SELECT_TRAINING_TYPE,
    SELECT_DURATION_FOR_IND_TRAIN,
    SELECT_PRECISE_IND_TIME,
    PERMISSION_FOR_IND_TRAIN,
    CONFIRM_GROUP_LESSON,
    SHOW_INFO_ABOUT_SKIPPING_DAY, TAKE_LESSON_BUTTON, CLNDR_IGNORE, CLNDR_DAY, CLNDR_PREV_MONTH, CLNDR_NEXT_MONTH,
    CLNDR_ACTION_BACK, CLNDR_ACTION_SKIP, CLNDR_ACTION_TAKE_GROUP, CLNDR_ACTION_TAKE_IND, SELECT_SKIP_TIME_BUTTON,
    BACK_BUTTON, from_digit_to_month, PAYMENT_VISITING, PAYMENT_BONUS, PAYMENT_MONEY, NO_PAYMENT_BUTTON,
    SUCCESS_PAYMENT,
)
from calendar import monthrange
from tennis_bot.config import ADMIN_TELEGRAM_TOKEN
from datetime import date, datetime, timedelta
from django.db.models import Q, F

from telegram import (
    InlineKeyboardButton as inline_button,
    InlineKeyboardMarkup as inline_markup,
)

import re
import telegram
import calendar


def update_user_info(update, user):
    user_details = update.message.from_user if update.message else None

    if user_details:
        user.is_blocked = False
        user.telegram_username = user_details.username[:64] if user_details.username else ''
        user.save()


@handler_decor()
def start(bot, update, user):
    update_user_info(update, user)
    bot.send_message(user.id, 'Я здесь', reply_markup=construct_main_menu(user, user.status))


@handler_decor()
def get_help(bot, update, user):
    bot.send_message(user.id, 'По всем вопросам пиши @ta2asho.\n'
                              'Желательно описывать свою проблему со скриншотами.', reply_markup=construct_main_menu(user, user.status))


@handler_decor()
def get_personal_data(bot, update, user):
    text = update.message.text
    phone_number_candidate = re.findall(r'\d+', text)
    if phone_number_candidate:
        if len(phone_number_candidate[0]) != 11:
            bot.send_message(user.id, 'Неправильный формат данных, было введено {} цифр.'.
                             format(len(phone_number_candidate[0])))
        else:
            user.phone_number = int(phone_number_candidate[0])
            user.save()
            bot.send_message(user.id,
                             'Как только тренер подтвердит твою кандидатуру, я напишу.',
                             reply_markup=construct_main_menu())
            admin_bot = telegram.Bot(ADMIN_TELEGRAM_TOKEN)
            admins = User.objects.filter(is_staff=True)

            for admin in admins:
                admin_bot.send_message(admin.id,
                                       # todo: сделать вместо ссылки кнопки при отправке этого сообешния
                                       'Пришел новый клиент:\n<b>{}</b>\n<a href="http://vladlen82.fvds.ru/admin/base/user/{}/change/">Настроить данные </a>'.format(
                                           user, user.id),
                                       parse_mode='HTML')

    else:
        if user.last_name and user.first_name and user.phone_number:
            bot.send_message(user.id, 'Контактные данные уже есть.')
        else:
            last_name, first_name = text.split(' ')
            user.last_name = last_name
            user.first_name = first_name
            user.save()
            bot.send_message(user.id, 'Введи номер телефона в формате "89991112233" (11 цифр подряд).')


@handler_decor(check_status=True)
def user_main_info(bot, update, user):
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
    user_payment = Payment.objects.filter(player=user, player__status=User.STATUS_TRAINING, fact_amount=0,
                                          year=today_date.year - 2020, month=today_date.month)

    if user_payment.exists():
        payment_status = f'{NO_PAYMENT_BUTTON}\n'
    elif user.status != User.STATUS_TRAINING:
        payment_status = ''
    else:
        payment_status = f'{SUCCESS_PAYMENT}\n'

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

    bot.send_message(user.id,
                     text,
                     parse_mode='HTML',
                     reply_markup=construct_main_menu(user, user.status))


def process_calendar_selection(bot, update, user):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    """
    query = update.callback_query
    (purpose, action, year, month, day) = separate_callback_data(query.data)
    curr = datetime(int(year), int(month), 1)

    if purpose == CLNDR_ACTION_SKIP:
        highlight_dates = select_tr_days_for_skipping(user)
    elif purpose == CLNDR_ACTION_TAKE_GROUP:
        training_days = get_potential_days_for_group_training(user)
        highlight_dates = list(training_days.values_list('date', flat=True))
    elif re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose):
        highlight_dates = None

    if action == CLNDR_IGNORE:
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == CLNDR_DAY:
        bot_edit_message(bot, query.message.text, update)
        return True, purpose, datetime(int(year), int(month), int(day))
    elif action == CLNDR_PREV_MONTH:
        pre = curr - timedelta(days=1)
        bot_edit_message(bot, query.message.text, update, create_calendar(purpose, int(pre.year), int(pre.month),
                                                                          highlight_dates))
    elif action == CLNDR_NEXT_MONTH:
        ne = curr + timedelta(days=31)
        bot_edit_message(bot, query.message.text, update, create_calendar(purpose, int(ne.year), int(ne.month),
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
        bot_edit_message(bot, text, update, create_calendar(purpose, int(year), int(month), highlight_dates))

    else:
        bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    return False, purpose, []


@handler_decor(check_status=True)
def inline_calendar_handler(bot, update, user):
    selected, purpose, date_my = process_calendar_selection(bot, update, user)
    today_date = moscow_datetime(datetime.now()).date()
    if selected:
        date_comparison = date(date_my.year, date_my.month, date_my.day)
        if purpose == CLNDR_ACTION_SKIP:
            if date_comparison < today_date:
                text = 'Тренировка уже прошла, ее нельзя отменить.\n' \
                       '✅ -- дни, доступные для отмены.'
                markup = create_calendar(CLNDR_ACTION_SKIP, date_my.year, date_my.month,
                                         select_tr_days_for_skipping(user))
            else:
                training_days = GroupTrainingDay.objects.filter(Q(group__users__in=[user]) |
                                                                Q(visitors__in=[user]) |
                                                                Q(pay_visitors__in=[user]),
                                                                date=date_my).exclude(absent__in=[user]).select_related(
                    'group').order_by(
                    'id').distinct('id')
                if training_days.count():
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
                    markup = create_calendar(purpose, date_my.year, date_my.month, select_tr_days_for_skipping(user))

        elif purpose == CLNDR_ACTION_TAKE_GROUP:
            training_days = get_potential_days_for_group_training(user)
            highlight_dates = list(training_days.values_list('date', flat=True))
            if date_comparison < today_date:
                text = 'Тренировка уже прошла, на нее нельзя записаться.\n' \
                       '✅ -- дни, доступные для групповых тренировок'
                markup = create_calendar(purpose, date_my.year, date_my.month, highlight_dates)
            else:
                training_days = training_days.filter(date=date_comparison)
                if training_days.count():
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

        bot_edit_message(bot, text, update, markup)


@handler_decor(check_status=True)
def skip_lesson_main_menu_button(bot, update, user):
    available_grouptraining_dates = select_tr_days_for_skipping(user)
    if available_grouptraining_dates:
        bot.send_message(user.id,
                         'Выбери дату тренировки для отмены.\n'
                         '✅ -- дни, доступные для отмены.',
                         reply_markup=create_calendar(CLNDR_ACTION_SKIP,
                                                      dates_to_highlight=available_grouptraining_dates))
    else:
        bot.send_message(user.id,
                         'Пока что нечего пропускать.',
                         reply_markup=construct_main_menu(user, user.status))


@handler_decor(check_status=True)
def skip_lesson_whem_geq_2(bot, update, user):
    tr_day_id = update.callback_query.data[len(SELECT_SKIP_TIME_BUTTON):]
    training_day = GroupTrainingDay.objects.get(id=tr_day_id)

    group_name, group_players = make_group_name_group_players_info_for_skipping(training_day)
    markup, text = construct_detail_menu_for_skipping(training_day, CLNDR_ACTION_SKIP, group_name, group_players)
    bot_edit_message(bot, text, update, markup)


@handler_decor(check_status=True)
def skip_lesson(bot, update, user):
    tr_day_id = update.callback_query.data[len(SHOW_INFO_ABOUT_SKIPPING_DAY):]
    training_day = GroupTrainingDay.objects.get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(training_day)
    if not training_day.is_available:
        text = "{} в {} ❌нет тренировки❌, т.к. она отменена тренером, поэтому ее нельзя пропустить.".format(date_tlg, time_tlg)
        bot_edit_message(bot, text, update)

        skip_lesson_main_menu_button(bot, update)

    else:
        if datetime.combine(training_day.date, training_day.start_time) - moscow_datetime(datetime.now()) < user.time_before_cancel:
            text = f'Неа, уже нельзя отменить занятие.' \
                   f' Количество часов, за которое тебе нужно отменять: {round(user.time_before_cancel.seconds/3600)}'
        else:
            text = 'Окей, занятие <b>{}</b> в <b>{}</b> отменено'.format(date_tlg, time_tlg)

            if training_day.is_individual:
                admin_bot = telegram.Bot(ADMIN_TELEGRAM_TOKEN)
                training_day.delete()
                admins = User.objects.filter(is_superuser=True, is_blocked=False)

                admin_text = f'⚠️ATTENTION⚠️\n' \
                       f'{user.first_name} {user.last_name} отменил индивидуальную тренировку\n' \
                       f'📅Дата: <b>{date_tlg} ({day_of_week})</b>\n' \
                       f'⏰Время: <b>{time_tlg}</b>\n\n'

                send_message(admins, admin_text, admin_bot)

            else:
                # проверяем его ли эта группа или он удаляется из занятия другой группы
                if user in training_day.visitors.all():
                    training_day.visitors.remove(user)
                    if user.status == User.STATUS_ARBITRARY:
                        user.bonus_lesson -= 1
                        user.save()
                elif user in training_day.pay_visitors.all():
                    training_day.pay_visitors.remove(user)
                    user.bonus_lesson -= 1
                    user.save()
                    # сначала убавляем, потом прибавляем
                else:
                    training_day.absent.add(user)

            user.bonus_lesson += 1
            user.save()

        bot_edit_message(bot, text, update)


@handler_decor(check_status=True)
def choose_type_of_training(bot, update, user):
    markup = inline_markup([[
        inline_button('Индивидуальная', callback_data=SELECT_TRAINING_TYPE + 'ind')
    ], [
        inline_button('Групповая', callback_data=SELECT_TRAINING_TYPE + 'group')
    ]])
    text = 'Выбери тип тренировки.'
    if update.callback_query:
        bot_edit_message(bot, text, update, markup)
    else:
        bot.send_message(user.id,
                         text,
                         reply_markup=markup)


@handler_decor(check_status=True)
def take_lesson(bot, update, user):
    """записаться на тренировку"""
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
        buttons = [[
            inline_button('1 час', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.0')
        ], [
            inline_button('1.5 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.5')
        ], [
            inline_button('2 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '2.0')
        ], [
            inline_button(f'{BACK_BUTTON}',
                          callback_data=TAKE_LESSON_BUTTON),
        ]]
        markup = inline_markup(buttons)
        text = 'Выбери продолжительность занятия'

    bot_edit_message(bot, text, update, markup)


@handler_decor()
def select_dt_for_ind_lesson(bot, update, user):
    duration = float(update.callback_query.data[len(SELECT_DURATION_FOR_IND_TRAIN):])
    markup = create_calendar(f'{CLNDR_ACTION_TAKE_IND}{duration}')
    text = 'Выбери дату тренировки.'
    bot_edit_message(bot, text, update, markup)


@handler_decor()
def select_precise_ind_lesson_time(bot, update, user):
    day_dt, start_time, end_time = update.callback_query.data[len(SELECT_PRECISE_IND_TIME):].split('|')
    date_dt = datetime.strptime(day_dt, DT_BOT_FORMAT)
    st_time_obj = datetime.strptime(start_time, '%H:%M:%S')
    end_time_obj = datetime.strptime(end_time, '%H:%M:%S')
    duration = end_time_obj - st_time_obj

    day_of_week = from_eng_to_rus_day_week[calendar.day_name[date_dt.date().weekday()]]

    group, _ = TrainingGroup.objects.get_or_create(name=user.first_name + user.last_name,
                                                   max_players=1)

    tr_day = GroupTrainingDay.objects.create(group=group, date=date_dt, start_time=st_time_obj, duration=duration,
                                             is_individual=True)

    text = f"Сообщу тренеру, что ты хочешь прийти на индивидуальное занятие"\
           f" <b>{day_dt} ({day_of_week}) </b>\n"\
           f"Время: <b>{start_time} — {end_time}</b>"
    bot_edit_message(bot, text, update)

    admin_bot = telegram.Bot(ADMIN_TELEGRAM_TOKEN)
    admins = User.objects.filter(is_staff=True, is_blocked=False)
    markup = inline_markup([[
        inline_button('Да', callback_data=f"{PERMISSION_FOR_IND_TRAIN}yes|{user.id}|{tr_day.id}")
    ], [
        inline_button('Нет', callback_data=f"{PERMISSION_FOR_IND_TRAIN}no|{user.id}|{tr_day.id}")
    ]])
    text = f"<b>{user.first_name} {user.last_name} — {user.phone_number}</b>\n" \
           f"Хочет прийти на индивидуальное занятие <b>{day_dt} ({day_of_week}) </b>" \
           f" в <b>{start_time} — {end_time}</b>\n" \
           f"<b>Разрешить?</b>"

    send_message(admins, text, admin_bot, markup=markup)


@handler_decor()
def select_precise_group_lesson_time(bot, update, user):
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
    n_free_places = tr_day.group.max_players - tr_day.pay_visitors.count() - tr_day.visitors.count() + \
                    tr_day.absent.count() - tr_day.group.users.count()
    all_players = tr_day.group.users.union(tr_day.visitors.all(), tr_day.pay_visitors.all()) \
        .difference(tr_day.absent.all()).values('first_name', 'last_name')
    text = ''
    if n_free_places <= 0 and tr_day.group.max_players < 6 and tr_day.group.available_for_additional_lessons:
        text = f'⚠️ATTENTION⚠️\n' \
               f'<b>Это занятие платное!</b>\n\n'
    group_level = {TrainingGroup.LEVEL_ORANGE: '🟠оранжевый мяч🟠', TrainingGroup.LEVEL_GREEN: '🟢зелёный мяч🟢'}

    all_players = '\n'.join((f"{x['first_name']} {x['last_name']}" for x in all_players))
    text += f'{tr_day.group.name} -- {group_level[tr_day.group.level]}\n' \
           f'📅Дата: <b>{date_tlg} ({day_of_week})</b>\n' \
           f'⏰Время: <b>{time_tlg}</b>\n\n' \
           f'👥Присутствующие:\n{all_players}\n\n' \
           f'Свободные места: {n_free_places if n_free_places > 0 else "есть за деньги"}'

    markup = inline_markup([[
        inline_button('Записаться', callback_data=f"{CONFIRM_GROUP_LESSON}{tr_day_id}")
    ], [
        inline_button(f'{BACK_BUTTON}',
                      callback_data=create_callback_data(CLNDR_ACTION_TAKE_GROUP, CLNDR_DAY, tr_day.date.year,
                                                         tr_day.date.month, tr_day.date.day))
    ]])

    bot_edit_message(bot, text, update, markup)


@handler_decor()
def confirm_group_lesson(bot, update, user):
    tr_day_id = update.callback_query.data[len(CONFIRM_GROUP_LESSON):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)

    time_tlg, start_time_tlg, end_time_tlg, date_tlg, day_of_week, start_time, end_time = get_time_info_from_tr_day(
        tr_day)
    n_free_places = tr_day.group.max_players - tr_day.visitors.distinct().count() + \
                    tr_day.absent.distinct().count() - tr_day.group.users.distinct().count()
    admit_message_text = ''
    if user in tr_day.absent.all():
        tr_day.absent.remove(user)
        text = f'Сначала отменять, а потом записываться, мда 🤦🏻‍♂️🥴. Вот почему я скоро буду управлять кожаными ' \
               f'мешками.\n' \
               f'Ладно, записал тебя на <b>{date_tlg} ({day_of_week})</b>\n' \
               f'Время: <b>{time_tlg}</b>'
        markup = None

        if user.bonus_lesson > 0:
            user.bonus_lesson -= 1
            user.save()

        else:
            admit_message_text = f'⚠️ATTENTION⚠️\n' \
                                 f'{user.first_name} {user.last_name} записался на <b>{date_tlg} ({day_of_week})</b>\n' \
                                 f'Время: <b>{time_tlg}</b>\n' \
                                 f'<b>Не за счет отыгрышей, не забудь взять с него денюжку.</b>'
    else:
        if user not in tr_day.group.users.all():
            if n_free_places > 0:
                tr_day.visitors.add(user)

                text = f'Записал тебя на <b>{date_tlg} ({day_of_week})</b>\n' \
                       f'Время: <b>{time_tlg}</b>'

                markup = None

                if user.bonus_lesson > 0 and user.status == User.STATUS_TRAINING:
                    user.bonus_lesson -= 1
                    user.save()

                else:
                    admit_message_text = f'⚠️ATTENTION⚠️\n' \
                                         f'{user.first_name} {user.last_name} записался на <b>{date_tlg} ({day_of_week})</b>\n' \
                                         f'Время: <b>{time_tlg}</b>\n' \
                                         f'<b>Не за счет отыгрышей, не забудь взять с него денюжку.</b>'

            else:
                if tr_day.group.available_for_additional_lessons and tr_day.group.max_players < 6:
                    tarif = StaticData.objects.first().tarif_arbitrary if user.status == User.STATUS_ARBITRARY \
                        else StaticData.objects.first().tarif_group
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
                        markup = inline_markup([[
                            inline_button(f'За отыгрыш + {StaticData.objects.first().tarif_payment_add_lesson}₽',
                                          callback_data=f"{PAYMENT_VISITING}{PAYMENT_BONUS}|{tr_day_id}")
                        ], [
                            inline_button(f'За {tarif}₽',
                                          callback_data=f"{PAYMENT_VISITING}{PAYMENT_MONEY}|{tr_day_id}")
                        ], [
                            inline_button(f'{BACK_BUTTON}',
                                          callback_data=f"{SELECT_PRECISE_GROUP_TIME}{tr_day_id}")
                        ]])
                else:
                    text = 'Упс, похоже уже не осталось свободных мест на это время, выбери другое.'
                    buttons = [[
                        inline_button(f'{BACK_BUTTON}',
                                      callback_data=create_callback_data(CLNDR_ACTION_TAKE_GROUP, CLNDR_DAY,
                                                                         tr_day.date.year, tr_day.date.month,
                                                                         tr_day.date.day))
                    ]]
                    markup = inline_markup(buttons)
        else:  # если пытается записаться в свою группу
            text = 'Ну ты чего?🤕 \nЭто же твоя группа, выбери другое время.'
            buttons = [[
                inline_button(f'{BACK_BUTTON}',
                              callback_data=SELECT_PRECISE_GROUP_TIME + f'{tr_day_id}')
            ]]
            markup = inline_markup(buttons)

    bot_edit_message(bot, text, update, markup)

    if admit_message_text:
        admin_bot = telegram.Bot(ADMIN_TELEGRAM_TOKEN)
        admins = User.objects.filter(is_staff=True, is_blocked=False)
        send_message(admins, admit_message_text, admin_bot)


@handler_decor()
def choose_type_of_payment_for_pay_visiting(bot, update, user):
    payment_choice, tr_day_id = update.callback_query.data[len(PAYMENT_VISITING):].split('|')
    tr_day = GroupTrainingDay.objects.get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    text, admin_text = '', ''
    if payment_choice == PAYMENT_BONUS:
        user.bonus_lesson -= 1
        user.save()

        tr_day.pay_visitors.add(user)
        text = f'Записал тебя на <b>{date_tlg} ({day_of_week})</b>\n' \
               f'Время: <b>{time_tlg}</b>\n' \
               f'⚠️ATTENTION⚠️\n' \
               f'Не забудь заплатить <b>{StaticData.objects.first().tarif_payment_add_lesson}₽</b>'

        admin_text = f'⚠️ATTENTION⚠️\n' \
                     f'{user.first_name} {user.last_name} записался на <b>{date_tlg} ({day_of_week})</b>\n' \
                     f'Время: <b>{time_tlg}</b>\n' \
                     f'<b>За счет платных отыгрешей, не забудь взять с него {StaticData.objects.first().tarif_payment_add_lesson}₽.</b>'

    elif payment_choice == PAYMENT_MONEY:
        tr_day.pay_visitors.add(user)
        tarif = StaticData.objects.first().tarif_arbitrary if user.status == User.STATUS_ARBITRARY \
            else StaticData.objects.first().tarif_group

        text = f'Записал тебя на <b>{date_tlg} ({day_of_week})</b>\n' \
               f'Время: <b>{time_tlg}</b>\n' \
               f'⚠️ATTENTION⚠️\n' \
               f'Не забудь заплатить <b>{tarif}₽</b>'

        admin_text = f'⚠️ATTENTION⚠️\n' \
                     f'{user.first_name} {user.last_name} записался на <b>{date_tlg} ({day_of_week})</b>\n' \
                     f'Время: <b>{time_tlg}</b>\n' \
                     f'<b>В дополнительное время, не забудь взять с него {tarif}₽.</b>'

    bot_edit_message(bot, text, update)

    admin_bot = telegram.Bot(ADMIN_TELEGRAM_TOKEN)
    admins = User.objects.filter(is_staff=True, is_blocked=False)
    send_message(admins, admin_text, admin_bot)


def make_group_name_group_players_info_for_skipping(tr_day):
    all_players = tr_day.group.users.union(tr_day.visitors.all(), tr_day.pay_visitors.all()).\
        difference(tr_day.absent.all()).\
            values('first_name', 'last_name')

    all_players = '\n'.join((f"{x['first_name']} {x['last_name']}" for x in all_players))

    if not tr_day.is_individual:
        group_name = f"{tr_day.group.name}\n"
        group_players = f'Присутствующие:\n{all_players}\n'
    else:
        group_name = "🧞‍♂индивидуальная тренировка🧞‍♂️\n"
        group_players = ''
    return group_name, group_players

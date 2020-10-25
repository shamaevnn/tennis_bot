import calendar

from telegram.ext import ConversationHandler
from django.core.exceptions import ObjectDoesNotExist
from base.models import User, GroupTrainingDay, Payment, TrainingGroup
from base.utils import construct_admin_main_menu, DT_BOT_FORMAT, TM_TIME_SCHEDULE_FORMAT, construct_menu_months, \
    construct_menu_groups, from_digit_to_month, moscow_datetime
from tele_interface.manage_data import PERMISSION_FOR_IND_TRAIN, SHOW_GROUPDAY_INFO, \
    from_eng_to_rus_day_week, CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, CLNDR_NEXT_MONTH, CLNDR_DAY, CLNDR_IGNORE, \
    CLNDR_PREV_MONTH, ADMIN_SITE, PAYMENT_YEAR, PAYMENT_YEAR_MONTH, PAYMENT_YEAR_MONTH_GROUP, PAYMENT_START_CHANGE, \
    PAYMENT_CONFIRM_OR_CANCEL
from tele_interface.utils import create_calendar, separate_callback_data, create_callback_data
from .utils import admin_handler_decor, day_buttons_coach_info
from tennis_bot.config import TELEGRAM_TOKEN
from datetime import date, datetime, timedelta
from telegram import (InlineKeyboardButton as inlinebutt,
                      InlineKeyboardMarkup as inlinemark, InlineKeyboardButton)

import datetime
import telegram


@admin_handler_decor()
def start(bot, update, user):
    update.message.reply_text(
        "Привет! я переехал на @TennisTula_bot",
        parse_mode='HTML',
        reply_markup=construct_admin_main_menu(),
    )


@admin_handler_decor()
def permission_for_ind_train(bot, update, user):
    permission, user_id, tr_day_id = update.callback_query.data[len(PERMISSION_FOR_IND_TRAIN):].split('|')

    tennis_bot = telegram.Bot(TELEGRAM_TOKEN)

    player = User.objects.get(id=user_id)

    tr_day = GroupTrainingDay.objects.filter(id=tr_day_id)

    if tr_day.count():
        tr_day = tr_day.first()
        start_time = tr_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
        end_time = (datetime.datetime.combine(tr_day.date, tr_day.start_time) + tr_day.duration).time().strftime(
            TM_TIME_SCHEDULE_FORMAT)

        if permission == 'yes':
            admin_text = 'Отлично, приятной тренировки!'

            user_text = f'Отлично, тренер подтвердил тренировку <b>{tr_day.date.strftime(DT_BOT_FORMAT)}</b>\n' \
                        f'Время: <b>{start_time} — {end_time}</b>\n' \
                        f'Не забудь!'

        else:
            admin_text = 'Хорошо, сообщу {} {}, что тренировка  {} \n<b>{} — {}</b> отменена.'.format(player.last_name,
                                                                                                      player.first_name,
                                                                                                      tr_day.date.strftime(
                                                                                                          DT_BOT_FORMAT),
                                                                                                      start_time,
                                                                                                      end_time)

            user_text = f'Внимание!!!\nИндивидуальная тренировка <b> {tr_day.date.strftime(DT_BOT_FORMAT)}</b>\n' \
                        f'в <b>{start_time} — {end_time}</b>\n' \
                        f'<b>ОТМЕНЕНА</b>'

            tr_day.delete()

        tennis_bot.send_message(
            player.id,
            user_text,
            parse_mode='HTML'
        )

    else:
        admin_text = 'Тренировка уже отменена.'

    bot.edit_message_text(
        admin_text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        parse_mode='HTML',
    )


def admin_calendar_selection(bot, update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    """
    query = update.callback_query
    (purpose, action, year, month, day) = separate_callback_data(query.data)
    curr = date(int(year), int(month), 1)

    if action == CLNDR_IGNORE:
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == CLNDR_DAY:
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id
                              )
        return True, purpose, date(int(year), int(month), int(day))
    elif action == CLNDR_PREV_MONTH:
        pre = curr - timedelta(days=1)
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(purpose, int(pre.year), int(pre.month)))
    elif action == CLNDR_NEXT_MONTH:
        ne = curr + timedelta(days=31)
        bot.edit_message_text(text=query.message.text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(purpose, int(ne.year), int(ne.month)))
    elif action == CLNDR_ACTION_BACK:
        if purpose == CLNDR_ADMIN_VIEW_SCHEDULE:
            text = 'Тренировочные дни'
        else:
            text = 'Тренировочные дни'

        bot.edit_message_text(text=text,
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                              reply_markup=create_calendar(purpose, int(year), int(month)))
    else:
        bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    return False, purpose, []


@admin_handler_decor()
def inline_calendar_handler(bot, update, user):
    selected, purpose, date_my = admin_calendar_selection(bot, update)
    if selected:
        if purpose == CLNDR_ADMIN_VIEW_SCHEDULE:
            tr_days = GroupTrainingDay.objects.filter(date=date_my).select_related('group').order_by('start_time')
            if tr_days.count():
                markup = day_buttons_coach_info(tr_days, SHOW_GROUPDAY_INFO)

                day_of_week = from_eng_to_rus_day_week[calendar.day_name[date_my.weekday()]]
                text = '📅{} ({})'.format(date_my, day_of_week)
            else:
                text = 'Нет тренировок в этот день'
                markup = create_calendar(purpose, date_my.year, date_my.month)
        bot.edit_message_text(text,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              reply_markup=markup,
                              parse_mode='HTML')


@admin_handler_decor()
def show_coach_schedule(bot, update, user):
    bot.send_message(user.id,
                     'Тренировочные дни',
                     reply_markup=create_calendar(CLNDR_ADMIN_VIEW_SCHEDULE))


@admin_handler_decor()
def redirect_to_site(bot, update, user):
    buttons = [[
        InlineKeyboardButton('Сайт', url='http://vladlen82.fvds.ru/admin/base/'),
    ]]
    bot.send_message(user.id,
                     ADMIN_SITE,
                     reply_markup=inlinemark(buttons))


def info_about_users(users, for_admin=False, payment=False):
    """
    :param payment: info about payment or not
    :param for_admin: show info for admin or not (number instead of smile)
    :param users: User instance
    :return: (first_name + last_name + \n){1,} -- str
    """
    if for_admin:
        if payment:
            return '\n'.join(
                (f"<b>{x['id']}</b>. {x['player__first_name']} {x['player__last_name']} -- {x['fact_amount']}₽,"
                 f" {x['theory_amount']}₽, {x['n_fact_visiting']}"
                 for x in users.values('player__first_name', 'player__last_name', 'fact_amount', 'theory_amount',
                                       'n_fact_visiting', 'id')))
        else:
            return '\n'.join(
                (f"{i + 1}. {x['first_name']} {x['last_name']}" for i, x in enumerate(users.values('first_name',
                                                                                                   'last_name'))))
    else:
        return '\n'.join(
            (f"👤{x['first_name']} {x['last_name']}" for x in users.values('first_name', 'last_name')))


@admin_handler_decor()
def show_traingroupday_info(bot, update, user):
    tr_day_id = update.callback_query.data[len(SHOW_GROUPDAY_INFO):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)

    availability = '❌нет тренировки❌\n' if not tr_day.is_available else ''
    is_individual = '🧑🏻‍🦯индивидуальная🧑🏻‍🦯\n' if tr_day.is_individual else '🤼‍♂️групповая🤼‍♂️\n'
    affiliation = '🧔🏻моя тренировка🧔🏻\n\n' if tr_day.tr_day_status == GroupTrainingDay.MY_TRAIN_STATUS else '👥аренда👥\n\n'

    group_name = f"{tr_day.group.name}\n"

    if not tr_day.is_individual:
        group_players = f'Игроки группы:\n{info_about_users(tr_day.group.users.all().difference(tr_day.absent.all()), for_admin=True)}\n'
        visitors = f'\n➕Пришли из других:\n{info_about_users(tr_day.visitors, for_admin=True)}\n' if tr_day.visitors.count() else ''
        absents = f'\n➖Отсутствуют:\n{info_about_users(tr_day.absent, for_admin=True)}\n' if tr_day.absent.count() else ''
    else:
        group_players = ''
        visitors = ''
        absents = ''

    end_time = datetime.datetime.combine(tr_day.date, tr_day.start_time) + tr_day.duration
    time = f'{tr_day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}'
    day_of_week = from_eng_to_rus_day_week[calendar.day_name[tr_day.date.weekday()]]

    general_info = f'<b>{tr_day.date.strftime(DT_BOT_FORMAT)} ({day_of_week})\n{time}</b>' + '\n' + availability + is_individual + affiliation
    users_info = group_name + group_players + visitors + absents
    text = general_info + users_info

    buttons = [[
        inlinebutt('⬅️ назад',
                   callback_data=create_callback_data(CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_DAY, tr_day.date.year,
                                                      tr_day.date.month, tr_day.date.day)),
    ]]

    bot.edit_message_text(text,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML',
                          reply_markup=inlinemark(buttons))


@admin_handler_decor()
def start_payment(bot, update, user):
    text = 'Выбери год'
    now_date = moscow_datetime(datetime.datetime.now()).date()
    buttons = [[
        inlinebutt('2020', callback_data=f'{PAYMENT_YEAR}0')
        ,
        inlinebutt('2021', callback_data=f'{PAYMENT_YEAR}1')
    ], [
        inlinebutt('К группам', callback_data=f'{PAYMENT_YEAR_MONTH}{now_date.year-2020}|{now_date.month}')
    ]]
    if update.callback_query:
        bot.edit_message_text(text,
                              chat_id=update.callback_query.message.chat_id,
                              message_id=update.callback_query.message.message_id,
                              parse_mode='HTML',
                              reply_markup=inlinemark(buttons))
    else:
        bot.send_message(user.id,
                         text,
                         reply_markup=inlinemark(buttons))


@admin_handler_decor()
def year_payment(bot, update, user):
    year = update.callback_query.data[len(PAYMENT_YEAR):]
    text = 'Выбери месяц'
    buttons = construct_menu_months(Payment.MONTHS, f'{PAYMENT_YEAR_MONTH}{year}|')
    bot.edit_message_text(text,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML',
                          reply_markup=buttons)


@admin_handler_decor()
def month_payment(bot, update, user):
    year, month = update.callback_query.data[len(PAYMENT_YEAR_MONTH):].split('|')
    text = f'{int(year)+2020}--{from_digit_to_month[int(month)]}\nВыбери группу'
    banda_groups = TrainingGroup.objects.filter(name__iregex=r'БАНДА')
    buttons = construct_menu_groups(banda_groups, f'{PAYMENT_YEAR_MONTH_GROUP}{year}|{month}|')
    bot.edit_message_text(text,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML',
                          reply_markup=buttons)

    return ConversationHandler.END


@admin_handler_decor()
def group_payment(bot, update, user):
    year, month, group_id = update.callback_query.data[len(PAYMENT_YEAR_MONTH_GROUP):].split('|')

    if int(group_id) == 0:
        title = 'Оставшиеся\n\n'
        payments = Payment.objects.filter(month=month, year=year).exclude(player__traininggroup__name__iregex='БАНДА')

    else:
        payments = Payment.objects.filter(player__traininggroup__id=group_id, month=month, year=year)
        group = TrainingGroup.objects.get(id=group_id)
        title = f'{group.name}\n\n'

    for payment in payments:
        payment.save()
    text = title + '<b>id</b>. Имя Фамилия -- факт₽, теория₽, кол-во посещений\n\n' + info_about_users(payments,
                                                                                                       for_admin=True,
                                                                                                       payment=True)

    markup = inlinemark([[
        inlinebutt('Изменить данные', callback_data=f'{PAYMENT_START_CHANGE}{year}|{month}|{group_id}')
    ], [
        inlinebutt('⬅️ назад', callback_data=f'{PAYMENT_YEAR_MONTH}{year}|{month}')
    ]])

    bot.edit_message_text(text,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML',
                          reply_markup=markup)


START_CHANGE_PAYMENT, CONFIRM_OR_CANCEL = range(2)


@admin_handler_decor()
def change_payment_data(bot, update, user):
    year, month, _ = update.callback_query.data[len(PAYMENT_START_CHANGE):].split('|')
    text = 'Для того, чтобы внести данные об оплате, введи данные в формате \n\n' \
           'id сумма_в_рублях через пробел, например, 18 3600\n\n'

    markup = inlinemark([[
        inlinebutt(f'{int(year) + 2020} -- {from_digit_to_month[int(month)]}',
                   callback_data=f'{PAYMENT_YEAR_MONTH}{year}|{month}')
    ]])

    bot.send_message(user.id,
                     text,
                     reply_markup=markup)
    return START_CHANGE_PAYMENT


@admin_handler_decor()
def get_id_amount(bot, update, user):
    try:
        payment_id, amount = update.message.text.split(' ')
        payment_id = int(payment_id)
        amount = int(amount)
        payment = Payment.objects.select_related('player').get(id=payment_id)

        text = f'{payment.player.first_name} {payment.player.last_name}\n' \
               f'Год: {2020 + int(payment.year)}\n' \
               f'Месяц: {from_digit_to_month[int(payment.month)]}\n' \
               f'<b>{payment.fact_amount}₽ ➡ {amount}₽</b>'
        buttons = inlinemark([[
            inlinebutt('Подтвердить', callback_data=f'{PAYMENT_CONFIRM_OR_CANCEL}YES|{payment_id}|{amount}')
            ,
            inlinebutt('Отмена', callback_data=f'{PAYMENT_CONFIRM_OR_CANCEL}NO|{payment_id}|{payment_id}')
        ]])
        bot.send_message(user.id,
                         text,
                         reply_markup=buttons,
                         parse_mode='HTML')

    except ValueError:
        text = 'Ошибка, скорее всего неправильно ввел id или сумму -- не ввел через пробел или есть лишние символы\n/cancel'
        bot.send_message(user.id,
                         text)

    except ObjectDoesNotExist:
        text = 'Нет такого объекта в базе данных -- неправильный id\n/cancel'
        bot.send_message(user.id,
                         text)

    return CONFIRM_OR_CANCEL


@admin_handler_decor()
def confirm_or_cancel_changing_payment(bot, update, user):
    permission, payment_id, amount = update.callback_query.data[len(PAYMENT_CONFIRM_OR_CANCEL):].split('|')
    payment = Payment.objects.get(id=payment_id)
    if permission == 'NO':
        text = 'Ну как хочешь'
    else:
        payment.fact_amount = int(amount)
        payment.save()

        text = 'Изменения внесены'

    markup = inlinemark([[
        inlinebutt(f'{int(payment.year) + 2020} -- {from_digit_to_month[int(payment.month)]}',
                   callback_data=f'{PAYMENT_YEAR_MONTH}{payment.year}|{payment.month}')
    ]])

    bot.edit_message_text(text,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML',
                          reply_markup=markup)

    return ConversationHandler.END


@admin_handler_decor()
def cancel(bot, update, user):
    update.message.reply_text('Вот так вот, да?',
                              reply_markup=construct_admin_main_menu())

    return ConversationHandler.END

from pytz import timezone
from telegram import (ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton)
from tele_interface.manage_data import (
    ADMIN_TIME_SCHEDULE_BUTTON,
    MY_DATA_BUTTON,
    SKIP_LESSON_BUTTON,
    TAKE_LESSON_BUTTON, HELP_BUTTON, ADMIN_SITE, ADMIN_PAYMENT, PAYMENT_YEAR_MONTH_GROUP, PAYMENT_YEAR, BACK_BUTTON, )

import telegram

DTTM_BOT_FORMAT = '%Y.%m.%d.%H.%M'
DT_BOT_FORMAT = '%Y.%m.%d'
TM_HOUR_BOT_FORMAT = '%H'
TM_DAY_BOT_FORMAT = '%d'
TM_TIME_SCHEDULE_FORMAT = '%H:%M'


def send_message(users, message: str, bot, markup=None):
    """
    :param users: instance of User model, iterable object
    :param message: text
    :param bot: instance of telegram.Bot
    :param markup: telegram markup
    :return: send message to users in telegram bot
    """

    for user in users:
        try:
            bot.send_message(user.id,
                             message,
                             reply_markup=markup,
                             parse_mode='HTML')
        except (telegram.error.Unauthorized, telegram.error.BadRequest):
            user.is_blocked = True
            user.status = 'F'
            user.save()


def construct_main_menu():
    return ReplyKeyboardMarkup([
        [MY_DATA_BUTTON, HELP_BUTTON],
        [SKIP_LESSON_BUTTON, TAKE_LESSON_BUTTON]],
        resize_keyboard=True)


def construct_admin_main_menu():
    return ReplyKeyboardMarkup([
        [ADMIN_PAYMENT, ADMIN_TIME_SCHEDULE_BUTTON],
        [ADMIN_SITE]],
        resize_keyboard=True)


def send_alert_about_changing_tr_day_status(tr_day, new_is_available: bool, bot):
    group_members = tr_day.group.users.all()
    visitors = tr_day.visitors.all()

    if not new_is_available:
        text = 'Тренировка <b>{} в {}</b> отменена.'.format(tr_day.date,
                                                            tr_day.start_time)
    else:
        text = 'Тренировка <b>{} в {}</b> доступна, ура!'.format(tr_day.date,
                                                                 tr_day.start_time)

    send_message(group_members.union(visitors), text, bot, construct_main_menu())


def moscow_datetime(date_time):
    return date_time.astimezone(timezone('Europe/Moscow')).replace(tzinfo=None)


def construct_menu_months(months, button_text):
    buttons = []
    row = []
    for month_num, month in months:
        row.append(
            InlineKeyboardButton(f'{month}', callback_data=f'{button_text}{month_num}')
        )
        if len(row) >= 3:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=f'{ADMIN_PAYMENT}'),
    ])

    return InlineKeyboardMarkup(buttons)


def construct_menu_groups(groups, button_text):
    buttons = []
    row = []
    for group in groups:
        row.append(
            InlineKeyboardButton(f'{group.name}', callback_data=f'{button_text}{group.id}')
        )
        if len(row) >= 3:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([InlineKeyboardButton('Оставшиеся', callback_data=f'{button_text}{0}')])

    year, month, _ = button_text[len(PAYMENT_YEAR_MONTH_GROUP):].split('|')
    buttons.append([
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=f'{PAYMENT_YEAR}{year}'),
    ])
    return InlineKeyboardMarkup(buttons)
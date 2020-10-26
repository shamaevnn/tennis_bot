import calendar

from pytz import timezone
from telegram import (ReplyKeyboardMarkup)
from tele_interface.manage_data import (
    ADMIN_TIME_SCHEDULE_BUTTON,
    MY_DATA_BUTTON,
    SKIP_LESSON_BUTTON,
    TAKE_LESSON_BUTTON, HELP_BUTTON, ADMIN_SITE, ADMIN_PAYMENT, from_eng_to_rus_day_week, )

import telegram
import datetime

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


def bot_edit_message(bot, text, update, markup=None):
    bot.edit_message_text(text=text,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML',
                          reply_markup=markup)


def get_time_info_from_tr_day(tr_day):
    """
    :param tr_day: instance of GroupTrainingDay
    :return: end_time, start_time: datetime,
             *time_tlg: str, is used in buttons,
             day_of_week: str, russian name of day of week
    """
    start_time = tr_day.start_time
    start_time_tlg = start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
    end_time = datetime.datetime.combine(tr_day.date, start_time) + tr_day.duration
    end_time_tlg = end_time.strftime(TM_TIME_SCHEDULE_FORMAT)
    time_tlg = f'{start_time_tlg} — {end_time_tlg}'
    day_of_week = from_eng_to_rus_day_week[calendar.day_name[tr_day.date.weekday()]]
    date_tlg = tr_day.date.strftime(DT_BOT_FORMAT)

    return time_tlg, start_time_tlg, end_time_tlg, date_tlg, day_of_week, start_time, end_time

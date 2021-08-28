import calendar

from datetime import date, datetime

from pytz import timezone
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from base.common_for_bots.manage_data import CLNDR_IGNORE, CLNDR_DAY, CLNDR_PREV_MONTH, CLNDR_NEXT_MONTH
from base.common_for_bots.static_text import from_digit_to_month, from_eng_to_rus_day_week
from base.models import GroupTrainingDay

DTTM_BOT_FORMAT = '%Y.%m.%d.%H.%M'
DT_BOT_FORMAT = '%Y.%m.%d'
TM_HOUR_BOT_FORMAT = '%H'
TM_DAY_BOT_FORMAT = '%d'
TM_TIME_SCHEDULE_FORMAT = '%H:%M'


def get_players_for_tr_day(tr_day):
    group_members = tr_day.group.users.all()
    visitors = tr_day.visitors.all()
    pay_visitors = tr_day.pay_visitors.all()
    pay_bonus_visitors = tr_day.pay_bonus_visitors.all()
    return group_members.union(visitors, pay_visitors, pay_bonus_visitors)


def get_actual_players_without_absent(tr_day):
    return get_players_for_tr_day(tr_day).difference(tr_day.absent.all())


def get_n_free_places(tr_day):
    players = get_actual_players_without_absent(tr_day)
    return tr_day.group.max_players - players.count()


def moscow_datetime(date_time):
    return date_time.astimezone(timezone('Europe/Moscow')).replace(tzinfo=None)


def bot_edit_message(bot, text, update, markup=None):
    bot.edit_message_text(
        text=text,
        chat_id=update.callback_query.message.chat_id,
        message_id=update.callback_query.message.message_id,
        parse_mode='HTML',
        reply_markup=markup
    )


def get_time_info_from_tr_day(tr_day: GroupTrainingDay):
    """
    :param tr_day: instance of GroupTrainingDay
    :return: end_time, start_time: datetime,
             *time_tlg: str, is used in buttons,
             day_of_week: str, russian name of day of week
    """
    start_time = tr_day.start_time
    start_time_tlg = start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
    end_time = datetime.combine(tr_day.date, start_time) + tr_day.duration
    end_time_tlg = end_time.strftime(TM_TIME_SCHEDULE_FORMAT)
    time_tlg = f'{start_time_tlg} — {end_time_tlg}'
    day_of_week = from_eng_to_rus_day_week[calendar.day_name[tr_day.date.weekday()]]
    date_tlg = tr_day.date.strftime(DT_BOT_FORMAT)

    return time_tlg, start_time_tlg, end_time_tlg, date_tlg, day_of_week, start_time, end_time


def create_calendar(purpose_of_calendar, year=None, month=None, dates_to_highlight=None):
    """
    Create an inline keyboard with the provided year and month
    :param list of dates dates_to_highlight : date we should highlight, e.g. days available for skipping
    :param str purpose_of_calendar: e.g. skipping, taking lesson
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = moscow_datetime(datetime.now())
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    data_ignore = create_callback_data(purpose_of_calendar, CLNDR_IGNORE, year, month, 0)
    keyboard = []
    # First row - Month and Year
    row = [InlineKeyboardButton(from_digit_to_month[month] + " " + str(year), callback_data=data_ignore)]
    keyboard.append(row)
    # Second row - Week Days
    row = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                day_info = str(day)
                if dates_to_highlight and (date(year, month, day) in dates_to_highlight):
                    day_info = f'{str(day)}✅'
                row.append(
                    InlineKeyboardButton(
                        day_info,
                        callback_data=create_callback_data(
                            purpose_of_calendar, CLNDR_DAY, year, month, day
                        )
                    )
                )
        keyboard.append(row)
    # Last row - Buttons
    row = [
        InlineKeyboardButton("<", callback_data=create_callback_data(
            purpose_of_calendar, CLNDR_PREV_MONTH, year, month, day
        )),
        InlineKeyboardButton(" ", callback_data=data_ignore),
        InlineKeyboardButton(">", callback_data=create_callback_data(
            purpose_of_calendar, CLNDR_NEXT_MONTH, year, month, day
        ))
    ]
    keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)


def create_callback_data(purpose, action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([purpose, action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")
import calendar
import datetime
from datetime import date, datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.utils import moscow_datetime
from tele_interface.manage_data import CLNDR_IGNORE, CLNDR_DAY, CLNDR_PREV_MONTH, CLNDR_NEXT_MONTH, \
    SELECT_PRECISE_GROUP_TIME
from tele_interface.static_text import from_digit_to_month, BACK_BUTTON
from tele_interface.utils import create_callback_data


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
                row.append(InlineKeyboardButton(day_info, callback_data=create_callback_data(purpose_of_calendar,
                                                                                             CLNDR_DAY, year, month,
                                                                                             day)))
        keyboard.append(row)
    # Last row - Buttons
    row = [InlineKeyboardButton("<", callback_data=create_callback_data(purpose_of_calendar, CLNDR_PREV_MONTH, year,
                                                                        month, day)),
           InlineKeyboardButton(" ", callback_data=data_ignore),
           InlineKeyboardButton(">", callback_data=create_callback_data(purpose_of_calendar, CLNDR_NEXT_MONTH, year,
                                                                        month, day))]
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


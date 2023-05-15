from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.common_for_bots.manage_data import CLNDR_DAY
from admin_bot.view_schedule.manage_data import (
    CLNDR_ADMIN_VIEW_SCHEDULE,
    AVAILABLE_TRAIN_DAY_ACTION_CONFIRM,
    AVAILABLE_TRAIN_DAY_ACTION,
)
from base.common_for_bots.static_text import (
    BACK_BUTTON,
    CANCEL_BUTTON,
    AVAILABLE_BUTTON,
)
from base.common_for_bots.utils import create_callback_data, create_callback_data_time
from base.models import GroupTrainingDay


def show_grouptrainingday_confirm_keyboard(year, month, day, start_time, action):

    text: str = ""
    if action == GroupTrainingDay.AVAILABLE:
        text = AVAILABLE_BUTTON

    else:
        text = CANCEL_BUTTON

    buttons = [
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=create_callback_data(
                    CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_DAY, year, month, day
                ),
            ),
            InlineKeyboardButton(
                text,
                callback_data=create_callback_data_time(
                    AVAILABLE_TRAIN_DAY_ACTION,
                    action,
                    year,
                    month,
                    day,
                    start_time,
                ),
            ),
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def show_grouptrainingday_info_keyboard(tr_day: GroupTrainingDay):

    action = ""
    text = ""
    if tr_day.available_status != GroupTrainingDay.AVAILABLE:
        text = AVAILABLE_BUTTON
        action = GroupTrainingDay.AVAILABLE

    else:
        text = CANCEL_BUTTON
        action = GroupTrainingDay.CANCELLED

    buttons = [
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=create_callback_data(
                    CLNDR_ADMIN_VIEW_SCHEDULE,
                    CLNDR_DAY,
                    tr_day.date.year,
                    tr_day.date.month,
                    tr_day.date.day,
                ),
            ),
            InlineKeyboardButton(
                text,
                callback_data=create_callback_data_time(
                    AVAILABLE_TRAIN_DAY_ACTION_CONFIRM,
                    action,
                    tr_day.date.year,
                    tr_day.date.month,
                    tr_day.date.day,
                    tr_day.start_time,
                ),
            ),
        ]
    ]
    return InlineKeyboardMarkup(buttons)

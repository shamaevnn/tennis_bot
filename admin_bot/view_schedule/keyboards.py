from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.common_for_bots.manage_data import CLNDR_DAY
from admin_bot.view_schedule.manage_data import (
    CLNDR_ADMIN_VIEW_SCHEDULE,
    AVAILABLE_TRAIN_DAY_ACTION_CONFIRM,
    AVAILABLE_TRAIN_DAY_ACTION,
    SHOW_GROUPDAY_INFO,
)
from base.common_for_bots.static_text import (
    BACK_BUTTON,
    CANCEL_BUTTON,
    AVAILABLE_BUTTON,
    ERROR_UNKNOWN_AVAILABLE_STATUS,
)
from base.common_for_bots.utils import create_callback_data, create_callback_data_id
from base.models import GroupTrainingDay


def show_grouptrainingday_available_change_confirm_keyboard(action, tr_day_id):

    text: str = ""
    if action == GroupTrainingDay.AVAILABLE:
        text = AVAILABLE_BUTTON

    elif action == GroupTrainingDay.CANCELLED:
        text = CANCEL_BUTTON

    elif action == GroupTrainingDay.NOT_AVAILABLE:
        text = CANCEL_BUTTON
    else:
        raise ValueError(ERROR_UNKNOWN_AVAILABLE_STATUS.format(action))

    buttons = [
        [
            InlineKeyboardButton(
                text=BACK_BUTTON, callback_data=f"{SHOW_GROUPDAY_INFO}{tr_day_id}"
            ),
            InlineKeyboardButton(
                text,
                callback_data=create_callback_data_id(
                    AVAILABLE_TRAIN_DAY_ACTION,
                    action,
                    tr_day_id,
                ),
            ),
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def show_grouptrainingday_available_change_keyboard(tr_day: GroupTrainingDay):

    action = ""
    text = ""
    if tr_day.available_status == GroupTrainingDay.CANCELLED:
        text = AVAILABLE_BUTTON
        action = GroupTrainingDay.AVAILABLE

    elif tr_day.available_status == GroupTrainingDay.NOT_AVAILABLE:
        text = AVAILABLE_BUTTON
        action = GroupTrainingDay.AVAILABLE

    elif tr_day.available_status == GroupTrainingDay.AVAILABLE:
        text = CANCEL_BUTTON
        action = GroupTrainingDay.CANCELLED
    else:
        raise ValueError(ERROR_UNKNOWN_AVAILABLE_STATUS.format(tr_day.available_status))

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
                callback_data=create_callback_data_id(
                    AVAILABLE_TRAIN_DAY_ACTION_CONFIRM,
                    action,
                    tr_day.id,
                ),
            ),
        ]
    ]
    return InlineKeyboardMarkup(buttons)

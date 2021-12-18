from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.common_for_bots.manage_data import CLNDR_DAY
from admin_bot.view_schedule.manage_data import CLNDR_ADMIN_VIEW_SCHEDULE
from base.common_for_bots.static_text import BACK_BUTTON
from base.common_for_bots.utils import create_callback_data


def back_from_show_grouptrainingday_info_keyboard(year, month, day):
    buttons = [
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=create_callback_data(
                    CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_DAY, year, month, day
                ),
            ),
        ]
    ]
    return InlineKeyboardMarkup(buttons)

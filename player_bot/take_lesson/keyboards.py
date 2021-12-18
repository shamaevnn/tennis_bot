import datetime
from datetime import datetime, timedelta
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.common_for_bots.utils import (
    DT_BOT_FORMAT,
    TM_TIME_SCHEDULE_FORMAT,
    create_callback_data,
)
from player_bot.take_lesson import manage_data
from player_bot.calendar.manage_data import CLNDR_ACTION_TAKE_IND
from base.common_for_bots.manage_data import CLNDR_ACTION_BACK
from player_bot.take_lesson.static_text import TYPE_IND, TYPE_GROUP, TYPE_RENT
from base.common_for_bots.static_text import BACK_BUTTON


def choose_type_of_training_keyboard():
    data = manage_data.SELECT_TRAINING_TYPE
    buttons = [
        [
            InlineKeyboardButton(
                TYPE_IND, callback_data=f"{data}{manage_data.TRAINING_IND}"
            )
        ],
        [
            InlineKeyboardButton(
                TYPE_GROUP, callback_data=f"{data}{manage_data.TRAINING_GROUP}"
            )
        ],
        [
            InlineKeyboardButton(
                TYPE_RENT, callback_data=f"{data}{manage_data.TRAINING_RENT}"
            )
        ],
    ]

    return InlineKeyboardMarkup(buttons)


def construct_time_menu_4ind_and_rent_lesson(
    button_data: str,
    poss_training_times: List[datetime.time],
    day_date: datetime.date,
    duration: float,
    back_button_data: str = CLNDR_ACTION_TAKE_IND,
) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for start_time in poss_training_times:
        end_time = datetime.combine(day_date, start_time) + timedelta(hours=duration)
        row.append(
            InlineKeyboardButton(
                text=f"{start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}",
                callback_data=f"{button_data}{day_date.strftime(DT_BOT_FORMAT)}|{start_time}|{end_time.time()}",
            )
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                text=BACK_BUTTON,
                callback_data=create_callback_data(
                    f"{back_button_data}{duration}",
                    CLNDR_ACTION_BACK,
                    day_date.year,
                    day_date.month,
                    0,
                ),
            )
        ]
    )
    return InlineKeyboardMarkup(buttons)

from datetime import datetime
from typing import Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.common_for_bots.manage_data import CLNDR_DAY
from base.common_for_bots.static_text import BACK_BUTTON
from base.common_for_bots.utils import create_callback_data
from player_bot.calendar.manage_data import CLNDR_ACTION_TAKE_RENT
from player_bot.take_lesson.rent import manage_data
from player_bot.take_lesson.rent.manage_data import SELECT_PRECISE_RENT_TIME
from player_bot.take_lesson.rent.static_text import RENT_COURT
from player_bot.take_lesson.static_text import TAKE_LESSON_BUTTON


def rent_choose_duration_keyboard() -> InlineKeyboardMarkup:
    data = manage_data.SELECT_DURATION_FOR_RENT
    buttons = [
        [InlineKeyboardButton("1 час", callback_data=f"{data}1.0")],
        [InlineKeyboardButton("1.5 часа", callback_data=f"{data}1.5")],
        [InlineKeyboardButton("2 часа", callback_data=f"{data}2.0")],
        [
            InlineKeyboardButton(BACK_BUTTON, callback_data=TAKE_LESSON_BUTTON),
        ],
    ]

    return InlineKeyboardMarkup(buttons)


def number_of_people_to_rent_cort_keyboard(
    training_time_data: str, duration: float, training_date: datetime
) -> InlineKeyboardMarkup:
    data = manage_data.NUMBER_OF_PEOPLE_TO_RENT_CORT
    buttons = [
        [
            InlineKeyboardButton("2", callback_data=f"{data}2|{training_time_data}"),
            InlineKeyboardButton("3", callback_data=f"{data}3|{training_time_data}"),
            InlineKeyboardButton("4", callback_data=f"{data}4|{training_time_data}"),
        ],
        [
            InlineKeyboardButton("5", callback_data=f"{data}5|{training_time_data}"),
            InlineKeyboardButton("6", callback_data=f"{data}6|{training_time_data}"),
        ],
        [
            InlineKeyboardButton(
                text=BACK_BUTTON,
                callback_data=create_callback_data(
                    purpose=f"{CLNDR_ACTION_TAKE_RENT}{duration}",
                    action=CLNDR_DAY,
                    year=training_date.year,
                    month=training_date.month,
                    day=training_date.day,
                ),
            )
        ],
    ]

    return InlineKeyboardMarkup(buttons)


def take_rent_lesson_or_back(
    number_of_players: Union[str, int], training_time_data: str
) -> InlineKeyboardMarkup:
    data = manage_data.TAKE_RENT_LESSON
    buttons = [
        [
            InlineKeyboardButton(
                RENT_COURT,
                callback_data=f"{data}{number_of_players}|{training_time_data}",
            )
        ],
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=f"{SELECT_PRECISE_RENT_TIME}{training_time_data}",
            ),
        ],
    ]

    return InlineKeyboardMarkup(buttons)

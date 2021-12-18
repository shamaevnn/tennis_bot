from typing import Union

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from admin_bot.ind_train import manage_data
from admin_bot.ind_train.static_text import YES, NO, SAVE_ONE_TRAIN, SAVE_FOR_TWO_MONTHS


def permission4ind_train_keyboard(
    tg_id: Union[str, int], tr_day_id: Union[str, int]
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=YES,
                callback_data=f"{manage_data.PERMISSION_FOR_IND_TRAIN}{manage_data.PERMISSION_YES}|{tg_id}|{tr_day_id}",
            ),
            InlineKeyboardButton(
                text=NO,
                callback_data=f"{manage_data.PERMISSION_FOR_IND_TRAIN}{manage_data.PERMISSION_NO}|{tg_id}|{tr_day_id}",
            ),
        ]
    ]

    return InlineKeyboardMarkup(buttons)


def how_many_trains_to_save_keyboard(tr_day_id: Union[str, int]):
    buttons = [
        [
            InlineKeyboardButton(
                text=SAVE_ONE_TRAIN,
                callback_data=f"{manage_data.AMOUNT_OF_IND_TRAIN}{tr_day_id}|{manage_data.AMOUNT_ONE}",
            )
        ],
        [
            InlineKeyboardButton(
                text=SAVE_FOR_TWO_MONTHS,
                callback_data=f"{manage_data.AMOUNT_OF_IND_TRAIN}{tr_day_id}|{manage_data.AMOUNT_MANY}",
            )
        ],
    ]

    return InlineKeyboardMarkup(buttons)

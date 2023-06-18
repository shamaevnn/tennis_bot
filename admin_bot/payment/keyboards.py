from typing import Union, Tuple, Dict

from django.db.models import QuerySet
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from admin_bot.payment.manage_data import PAYMENT_CHANGE_YES, PAYMENT_CHANGE_NO
from base.common_for_bots.static_text import from_digit_to_month, CONFIRM
from admin_bot.payment import static_text
from admin_bot.payment import manage_data
from base.common_for_bots.static_text import BACK_BUTTON
from base.models import TrainingGroup, Payment


def back_to_payment_groups_when_changing_payment_keyboard(
    year: Union[str, int], month: Union[str, int]
):
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{int(year) + 2020} — {from_digit_to_month[int(month)]}",
                callback_data=f"{manage_data.PAYMENT_YEAR_MONTH}{year}|{month}",
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def cancel_confirm_changing_payment_info_keyboard(
    payment_id: Union[str, int], amount: Union[str, int]
):
    buttons = [
        [
            InlineKeyboardButton(
                text=CONFIRM,
                callback_data=f"{manage_data.PAYMENT_CONFIRM_OR_CANCEL}{PAYMENT_CHANGE_YES}|{payment_id}|{amount}",
            ),
            InlineKeyboardButton(
                text=static_text.CANCEL,
                callback_data=f"{manage_data.PAYMENT_CONFIRM_OR_CANCEL}{PAYMENT_CHANGE_NO}|{payment_id}|{payment_id}",
            ),
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def change_payment_info_keyboard(
    payments_values: QuerySet[Dict],
    year: Union[str, int],
    month: Union[str, int],
    group_id: Union[str, int],
):
    player_info_buttons = [
        [
            InlineKeyboardButton(
                text=f"{payment['player__last_name']} {payment['player__first_name']}",
                callback_data=f"{manage_data.COACH_GET_PLAYER_INFO}{payment['id']}|{group_id}",
            )
            for payment in payments_values
        ]
    ]

    _buttons = [
        [
            InlineKeyboardButton(
                static_text.CHANGE_DATA,
                callback_data=f"{manage_data.PAYMENT_START_CHANGE}{year}|{month}|{group_id}",
            )
        ],
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=f"{manage_data.PAYMENT_YEAR_MONTH}{year}|{month}",
            )
        ],
    ]
    buttons = player_info_buttons + _buttons
    return InlineKeyboardMarkup(buttons)


def back_to_group_payment_from_player_info(
    year: Union[str, int],
    month: Union[str, int],
    group_id: int,
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=f"{manage_data.PAYMENT_YEAR_MONTH_GROUP}{year}|{month}|{group_id}",
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def choose_year_to_group_payment_keyboard(
    year: Union[str, int], month: Union[str, int]
):
    buttons = [
        [
            InlineKeyboardButton(
                static_text.YEAR_2020, callback_data=f"{manage_data.PAYMENT_YEAR}0"
            ),
            InlineKeyboardButton(
                static_text.YEAR_2021, callback_data=f"{manage_data.PAYMENT_YEAR}1"
            ),
            InlineKeyboardButton(
                static_text.YEAR_2022, callback_data=f"{manage_data.PAYMENT_YEAR}2"
            ),
            InlineKeyboardButton(
                static_text.YEAR_2023, callback_data=f"{manage_data.PAYMENT_YEAR}3"
            ),
        ],
        [
            InlineKeyboardButton(
                static_text.TO_GROUPS,
                callback_data=f"{manage_data.PAYMENT_YEAR_MONTH}{year - 2020}|{month}",
            )
        ],
    ]

    return InlineKeyboardMarkup(buttons)


def construct_menu_groups(groups: QuerySet[TrainingGroup], button_text: str):
    buttons = []
    row = []
    for group in groups:
        row.append(
            InlineKeyboardButton(group.name, callback_data=f"{button_text}{group.id}")
        )
        if len(row) >= 3:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                static_text.HAVE_NOT_PAID, callback_data=f"{button_text}{0}"
            )
        ]
    )

    year, month, _ = button_text[len(manage_data.PAYMENT_YEAR_MONTH_GROUP) :].split("|")
    buttons.append(
        [
            InlineKeyboardButton(
                BACK_BUTTON, callback_data=f"{manage_data.PAYMENT_YEAR}{year}"
            ),
        ]
    )

    return InlineKeyboardMarkup(buttons)


def construct_menu_months(months: Tuple[Tuple[str, str]], button_text: str):
    buttons = []
    row = []
    for month_num, month in months:
        row.append(
            InlineKeyboardButton(month, callback_data=f"{button_text}{month_num}")
        )
        if len(row) >= 3:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(BACK_BUTTON, callback_data=static_text.ADMIN_PAYMENT),
        ]
    )

    return InlineKeyboardMarkup(buttons)

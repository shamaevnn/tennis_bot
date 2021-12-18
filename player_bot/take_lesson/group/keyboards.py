from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.common_for_bots.manage_data import CLNDR_DAY, CLNDR_ACTION_BACK
from base.common_for_bots.static_text import BACK_BUTTON
from base.common_for_bots.utils import create_callback_data, get_time_info_from_tr_day
from player_bot.calendar.manage_data import CLNDR_ACTION_TAKE_GROUP
from player_bot.take_lesson.group import manage_data


def take_lesson_back_keyboard(tr_day_id, year, month, day):
    buttons = [
        [
            InlineKeyboardButton(
                "Записаться",
                callback_data=f"{manage_data.CONFIRM_GROUP_LESSON}{tr_day_id}",
            )
        ],
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=create_callback_data(
                    CLNDR_ACTION_TAKE_GROUP, CLNDR_DAY, year, month, day
                ),
            )
        ],
    ]

    return InlineKeyboardMarkup(buttons)


def choose_type_of_payment_for_group_lesson_keyboard(
    payment_add_lesson, tr_day_id, tarif
):
    buttons = [
        [
            InlineKeyboardButton(
                f"За отыгрыш + {payment_add_lesson}₽",
                callback_data=f"{manage_data.PAYMENT_VISITING}{manage_data.PAYMENT_MONEY_AND_BONUS_LESSONS}|{tr_day_id}",
            )
        ],
        [
            InlineKeyboardButton(
                f"За {tarif}₽",
                callback_data=f"{manage_data.PAYMENT_VISITING}{manage_data.PAYMENT_MONEY}|{tr_day_id}",
            )
        ],
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=f"{manage_data.SELECT_PRECISE_GROUP_TIME}{tr_day_id}",
            )
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def back_to_group_times_when_no_left_keyboard(year, month, day):
    """
    Создает клавиатура с кнопкой назад, когда в данном
    тренировочном дне на выбранное время уже нет
    свободных мест
    """
    buttons = [
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=create_callback_data(
                    purpose=CLNDR_ACTION_TAKE_GROUP,
                    action=CLNDR_DAY,
                    year=year,
                    month=month,
                    day=day,
                ),
            )
        ]
    ]
    return InlineKeyboardMarkup(buttons)


def construct_time_menu_for_group_lesson(button_text, tr_days, date, purpose):
    buttons = []
    row = []
    for day in tr_days:
        time_tlg, _, _, _, _, _, _ = get_time_info_from_tr_day(day)
        row.append(
            InlineKeyboardButton(f"{time_tlg}", callback_data=button_text + str(day.id))
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append(
        [
            InlineKeyboardButton(
                BACK_BUTTON,
                callback_data=create_callback_data(
                    purpose, CLNDR_ACTION_BACK, date.year, date.month, 0
                ),
            ),
        ]
    )

    return InlineKeyboardMarkup(buttons)

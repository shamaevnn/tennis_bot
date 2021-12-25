from collections import Counter

from django.db.models import QuerySet
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from admin_bot.send_message.static_text import TO_ALL_GROUPS, TO_ALL, TO_FREE_SCHEDULE
from base.common_for_bots.static_text import CONFIRM
from admin_bot.send_message.utils import handle_selecting_groups_to_send_message_to
from admin_bot.send_message.manage_data import (
    SEND_MESSAGE,
    ALL_GROUPS,
    CONFIRM_SENDING,
    SEND_TO_ALL,
    SEND_TO_ARBITRARY_SCHEDULE,
)
from base.models import TrainingGroup


def construct_menu_groups_for_send_message(
    groups: QuerySet[TrainingGroup], button_data: str
):
    group_ids = button_data[len(SEND_MESSAGE) :].split("|")
    ids_counter = Counter(group_ids)

    buttons = []
    row = []
    for group in groups:
        if str(group.id) not in group_ids:
            text_button = group.name
        elif ids_counter[str(group.id)] > 1 and ids_counter[str(group.id)] % 2 == 0:
            text_button = group.name
            group_ids.remove(str(group.id))
            group_ids.remove(str(group.id))
            button_data = button_data[: len(SEND_MESSAGE)] + "|".join(group_ids)
        else:
            text_button = group.name + " ✅"

        row.append(
            InlineKeyboardButton(
                f"{text_button}", callback_data=f"{button_data}|{group.id}"
            )
        )
        if len(row) >= 3:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    all_groups_text, button_data = handle_selecting_groups_to_send_message_to(
        ids_counter=ids_counter,
        group_ids=group_ids,
        group_id=ALL_GROUPS,
        button_data_text=button_data,
        button_text=TO_ALL_GROUPS,
    )
    all_text, button_data = handle_selecting_groups_to_send_message_to(
        ids_counter=ids_counter,
        group_ids=group_ids,
        group_id=SEND_TO_ALL,
        button_data_text=button_data,
        button_text=TO_ALL,
    )

    free_schedule, button_data = handle_selecting_groups_to_send_message_to(
        ids_counter=ids_counter,
        group_ids=group_ids,
        group_id=SEND_TO_ARBITRARY_SCHEDULE,
        button_data_text=button_data,
        button_text=TO_FREE_SCHEDULE,
    )

    buttons.append(
        [
            InlineKeyboardButton(
                all_groups_text, callback_data=f"{button_data}|{ALL_GROUPS}"
            ),
            InlineKeyboardButton(
                all_text, callback_data=f"{button_data}|{SEND_TO_ALL}"
            ),
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                free_schedule,
                callback_data=f"{button_data}|{SEND_TO_ARBITRARY_SCHEDULE}",
            )
        ]
    )
    buttons.append(
        [
            InlineKeyboardButton(
                CONFIRM, callback_data=f"{button_data}|{CONFIRM_SENDING}"
            )
        ]
    )

    return InlineKeyboardMarkup(buttons)

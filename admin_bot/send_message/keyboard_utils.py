from collections import Counter

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from admin_bot.static_text import TO_ALL_GROUPS, TO_ALL, TO_FREE_SCHEDULE, CONFIRM
from admin_bot.send_message.utils import handle_selecting_groups_to_send_message_to
from tele_interface.manage_data import SEND_MESSAGE


def construct_menu_groups_for_send_message(groups, button_text):
    group_ids = button_text[len(SEND_MESSAGE):].split("|")
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
            button_text = button_text[:len(SEND_MESSAGE)] + "|".join(group_ids)
        else:
            text_button = group.name + " ✅"

        row.append(
            InlineKeyboardButton(f'{text_button}', callback_data=f'{button_text}|{group.id}')
        )
        if len(row) >= 3:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    all_groups_text, button_text = handle_selecting_groups_to_send_message_to(
        ids_counter=ids_counter,
        group_ids=group_ids,
        group_id='0',
        button_data_text=button_text,
        button_text=TO_ALL_GROUPS
    )
    all_text, button_text = handle_selecting_groups_to_send_message_to(
        ids_counter=ids_counter,
        group_ids=group_ids,
        group_id='-2',
        button_data_text=button_text,
        button_text=TO_ALL
    )

    free_schedule, button_text = handle_selecting_groups_to_send_message_to(
        ids_counter=ids_counter,
        group_ids=group_ids,
        group_id='-3',
        button_data_text=button_text,
        button_text=TO_FREE_SCHEDULE
    )

    buttons.append([
        InlineKeyboardButton(all_groups_text, callback_data=f'{button_text}|{0}'),
        InlineKeyboardButton(all_text, callback_data=f'{button_text}|{-2}')]
    )
    buttons.append([
        InlineKeyboardButton(free_schedule, callback_data=f'{button_text}|{-3}')
    ])
    buttons.append([InlineKeyboardButton(CONFIRM, callback_data=f'{button_text}|{-1}')])

    return InlineKeyboardMarkup(buttons)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import base.common_for_bots.static_text
from admin_bot.payment import static_text
from admin_bot.payment import manage_data
from base.common_for_bots.static_text import BACK_BUTTON


def back_to_payment_groups_when_changing_payment_keyboard(year, month, from_digit_to_month_dict):
    buttons = [[
        InlineKeyboardButton(
            text=f'{int(year) + 2020} -- {from_digit_to_month_dict[int(month)]}',
            callback_data=f'{manage_data.PAYMENT_YEAR_MONTH}{year}|{month}'
        )
    ]]
    return InlineKeyboardMarkup(buttons)


def cancel_confirm_changing_payment_info_keyboard(payment_id, amount):
    buttons = [[
        InlineKeyboardButton(
            base.common_for_bots.static_text.CONFIRM, callback_data=f'{manage_data.PAYMENT_CONFIRM_OR_CANCEL}YES|{payment_id}|{amount}'
        ),
        InlineKeyboardButton(
            static_text.CANCEL, callback_data=f'{manage_data.PAYMENT_CONFIRM_OR_CANCEL}NO|{payment_id}|{payment_id}'
        )
    ]]
    return InlineKeyboardMarkup(buttons)


def change_payment_info_keyboard(year, month, group_id):
    buttons = [[
        InlineKeyboardButton(
            static_text.CHANGE_DATA, callback_data=f'{manage_data.PAYMENT_START_CHANGE}{year}|{month}|{group_id}'
        )
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}', callback_data=f'{manage_data.PAYMENT_YEAR_MONTH}{year}|{month}')
    ]]

    return InlineKeyboardMarkup(buttons)


def choose_year_to_group_payment_keyboard(year, month):
    buttons = [[
        InlineKeyboardButton(static_text.YEAR_2020, callback_data=f'{manage_data.PAYMENT_YEAR}0')
        ,
        InlineKeyboardButton(static_text.YEAR_2021, callback_data=f'{manage_data.PAYMENT_YEAR}1')
    ], [
        InlineKeyboardButton(
            static_text.TO_GROUPS, callback_data=f'{manage_data.PAYMENT_YEAR_MONTH}{year - 2020}|{month}'
        )
    ]]

    return InlineKeyboardMarkup(buttons)


def construct_menu_groups(groups, button_text):
    buttons = []
    row = []
    for group in groups:
        row.append(
            InlineKeyboardButton(f'{group.name}', callback_data=f'{button_text}{group.id}')
        )
        if len(row) >= 3:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([InlineKeyboardButton(static_text.HAVE_NOT_PAID, callback_data=f'{button_text}{0}')])

    year, month, _ = button_text[len(manage_data.PAYMENT_YEAR_MONTH_GROUP):].split('|')
    buttons.append([
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=f'{manage_data.PAYMENT_YEAR}{year}'),
    ])

    return InlineKeyboardMarkup(buttons)


def construct_menu_months(months, button_text):
    buttons = []
    row = []
    for month_num, month in months:
        row.append(
            InlineKeyboardButton(f'{month}', callback_data=f'{button_text}{month_num}')
        )
        if len(row) >= 3:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=f'{static_text.ADMIN_PAYMENT}'),
    ])

    return InlineKeyboardMarkup(buttons)

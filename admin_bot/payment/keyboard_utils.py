from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from admin_bot.static_text import CONFIRM, CANCEL, CHANGE_DATA, YEAR_2020, YEAR_2021, TO_GROUPS
from tele_interface.manage_data import PAYMENT_YEAR_MONTH, PAYMENT_CONFIRM_OR_CANCEL, PAYMENT_START_CHANGE, PAYMENT_YEAR
from tele_interface.static_text import BACK_BUTTON


def back_to_payment_groups_when_changing_payment_keyboard(year, month, from_digit_to_month_dict):
    buttons = [[
        InlineKeyboardButton(f'{int(year) + 2020} -- {from_digit_to_month_dict[int(month)]}',
                   callback_data=f'{PAYMENT_YEAR_MONTH}{year}|{month}')
    ]]

    return InlineKeyboardMarkup(buttons)


def cancel_confirm_changing_payment_info_keyboard(payment_id, amount):
    buttons = [[
        InlineKeyboardButton(CONFIRM, callback_data=f'{PAYMENT_CONFIRM_OR_CANCEL}YES|{payment_id}|{amount}')
        ,
        InlineKeyboardButton(CANCEL, callback_data=f'{PAYMENT_CONFIRM_OR_CANCEL}NO|{payment_id}|{payment_id}')
    ]]

    return InlineKeyboardMarkup(buttons)


def change_payment_info_keyboard(year, month, group_id):
    buttons = [[
        InlineKeyboardButton(CHANGE_DATA, callback_data=f'{PAYMENT_START_CHANGE}{year}|{month}|{group_id}')
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}', callback_data=f'{PAYMENT_YEAR_MONTH}{year}|{month}')
    ]]

    return InlineKeyboardMarkup(buttons)


def choose_year_to_group_payment_keyboard(year, month):
    buttons = [[
        InlineKeyboardButton(YEAR_2020, callback_data=f'{PAYMENT_YEAR}0')
        ,
        InlineKeyboardButton(YEAR_2021, callback_data=f'{PAYMENT_YEAR}1')
    ], [
        InlineKeyboardButton(TO_GROUPS, callback_data=f'{PAYMENT_YEAR_MONTH}{year - 2020}|{month}')
    ]]

    return InlineKeyboardMarkup(buttons)
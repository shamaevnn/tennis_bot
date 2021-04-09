from collections import Counter

from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from base.utils import get_time_info_from_tr_day, handle_selecting_groups_to_send_message_to
from tele_interface.manage_data import SEND_MESSAGE, CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, \
    PAYMENT_YEAR_MONTH_GROUP, PAYMENT_YEAR, PERMISSION_FOR_IND_TRAIN, PAYMENT_YEAR_MONTH, PAYMENT_CONFIRM_OR_CANCEL, \
    PAYMENT_START_CHANGE, CLNDR_DAY, AMOUNT_OF_IND_TRAIN
from tele_interface.static_text import BACK_BUTTON
from admin_bot.static_text import *
from tele_interface.utils import create_callback_data


def construct_admin_main_menu():
    return ReplyKeyboardMarkup([
        [ADMIN_PAYMENT, ADMIN_TIME_SCHEDULE_BUTTON],
        [ADMIN_SITE, ADMIN_SEND_MESSAGE]],
        resize_keyboard=True)


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

    buttons.append([
        InlineKeyboardButton(all_groups_text, callback_data=f'{button_text}|{0}'),
        InlineKeyboardButton(all_text, callback_data=f'{button_text}|{-2}')]
    )
    buttons.append([InlineKeyboardButton(CONFIRM, callback_data=f'{button_text}|{-1}')])

    return InlineKeyboardMarkup(buttons)


def day_buttons_coach_info(tr_days, button_text):
    buttons = []
    row = []
    for day in tr_days:
        time_tlg, _, _, _, _, _, _ = get_time_info_from_tr_day(day)
        row.append(
            InlineKeyboardButton(f'{day.group.name}', callback_data=f"{button_text}{day.id}")
        )
        row.append(
            InlineKeyboardButton(
                f'{time_tlg}',
                callback_data=f"{button_text}{day.id}")
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(f'{BACK_BUTTON}',
                   callback_data=create_callback_data(CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, tr_days.first().date.year, tr_days.first().date.month, 0)),
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
                             callback_data=f'{ADMIN_PAYMENT}'),
    ])

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

    buttons.append([InlineKeyboardButton(REST, callback_data=f'{button_text}{0}')])

    year, month, _ = button_text[len(PAYMENT_YEAR_MONTH_GROUP):].split('|')
    buttons.append([
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=f'{PAYMENT_YEAR}{year}'),
    ])

    return InlineKeyboardMarkup(buttons)


def yes_no_permission4ind_train_keyboard(user_id, tr_day_id):
    buttons = [[
        InlineKeyboardButton(YES, callback_data=f"{PERMISSION_FOR_IND_TRAIN}yes|{user_id}|{tr_day_id}"),
        InlineKeyboardButton(NO, callback_data=f"{PERMISSION_FOR_IND_TRAIN}no|{user_id}|{tr_day_id}")
    ]]

    return InlineKeyboardMarkup(buttons)


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


def back_from_show_grouptrainingday_info_keyboard(year, month, day):
    buttons = [[
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=create_callback_data(
                                 CLNDR_ADMIN_VIEW_SCHEDULE,
                                 CLNDR_DAY,
                                 year, month, day)),
    ]]

    return InlineKeyboardMarkup(buttons)


def how_many_trains_to_save_keyboard(tr_day_id):
    buttons = [[
        InlineKeyboardButton(SAVE_ONE_TRAIN, callback_data=f'{AMOUNT_OF_IND_TRAIN}{tr_day_id}|one')]
        ,
        [InlineKeyboardButton(SAVE_FOR_TWO_MONTHS, callback_data=f'{AMOUNT_OF_IND_TRAIN}{tr_day_id}|many')]
    ]

    return InlineKeyboardMarkup(buttons)


def go_to_site_keyboard():
    buttons = [[
        InlineKeyboardButton(SITE, url='http://vladlen82.fvds.ru/tgadmin/base/'),
    ]]

    return InlineKeyboardMarkup(buttons)


def go_to_site_set_up_personal_data(user_id):
    buttons = [[
        InlineKeyboardButton(SET_UP_DATA, url='http://vladlen82.fvds.ru/tgadmin/base/user/{}/change/'.format(user_id)),
    ]]

    return InlineKeyboardMarkup(buttons)

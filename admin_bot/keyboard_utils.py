from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from base.utils import get_time_info_from_tr_day
from tele_interface.manage_data import CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, \
    PAYMENT_YEAR_MONTH_GROUP, PAYMENT_YEAR, PERMISSION_FOR_IND_TRAIN, CLNDR_DAY, AMOUNT_OF_IND_TRAIN
from tele_interface.static_text import BACK_BUTTON
from admin_bot.static_text import *
from tele_interface.utils import create_callback_data


def construct_admin_main_menu():
    return ReplyKeyboardMarkup([
        [ADMIN_PAYMENT, ADMIN_TIME_SCHEDULE_BUTTON],
        [ADMIN_SITE, ADMIN_SEND_MESSAGE]],
        resize_keyboard=True)


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

    buttons.append([InlineKeyboardButton(HAVE_NOT_PAID, callback_data=f'{button_text}{0}')])

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

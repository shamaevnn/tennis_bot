from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from admin_bot.go_to_site.static_text import SET_UP_DATA, SITE


def go_to_site_keyboard():
    buttons = [[
        InlineKeyboardButton(SITE, url='https://vladlen82.fvds.ru/tgadmin/base/'),
    ]]

    return InlineKeyboardMarkup(buttons)


def go_to_site_set_up_personal_data(user_id):
    buttons = [[
        InlineKeyboardButton(SET_UP_DATA, url='https://vladlen82.fvds.ru/tgadmin/base/user/{}/change/'.format(user_id)),
    ]]

    return InlineKeyboardMarkup(buttons)
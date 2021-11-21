from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from admin_bot.go_to_site.static_text import SET_UP_DATA, SITE
from tennis_bot.settings import HOST


def go_to_site_keyboard():
    buttons = [[
        InlineKeyboardButton(SITE, url=HOST),
    ]]

    return InlineKeyboardMarkup(buttons)


def go_to_site_set_up_personal_data(player_id: str):
    buttons = [[
        InlineKeyboardButton(SET_UP_DATA, url=f'{HOST}player/{player_id}/change/'),
    ]]

    return InlineKeyboardMarkup(buttons)

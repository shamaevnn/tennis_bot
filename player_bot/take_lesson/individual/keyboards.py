from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from base.common_for_bots.static_text import BACK_BUTTON
from player_bot.take_lesson.individual import manage_data
from player_bot.take_lesson.static_text import TAKE_LESSON_BUTTON


def ind_train_choose_duration_keyboard():
    data = manage_data.SELECT_DURATION_FOR_IND_TRAIN
    buttons = [[
        InlineKeyboardButton('1 час', callback_data=f'{data}1.0')
    ], [
        InlineKeyboardButton('1.5 часа', callback_data=f'{data}1.5')
    ], [
        InlineKeyboardButton('2 часа', callback_data=f'{data}2.0')
    ], [
        InlineKeyboardButton(BACK_BUTTON, callback_data=TAKE_LESSON_BUTTON),
    ]]

    return InlineKeyboardMarkup(buttons)

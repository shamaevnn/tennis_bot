from telegram import InlineKeyboardButton as inlinebutt, InlineKeyboardMarkup as inlinemark, InlineKeyboardButton, \
    InlineKeyboardMarkup

from base.common_for_bots.utils import get_time_info_from_tr_day, create_callback_data
from player_bot.skip_lesson.manage_data import SELECT_SKIP_TIME_BUTTON, SHOW_INFO_ABOUT_SKIPPING_DAY
from player_bot.calendar.manage_data import CLNDR_ACTION_SKIP
from base.common_for_bots.manage_data import CLNDR_ACTION_BACK
from base.common_for_bots.static_text import BACK_BUTTON


def construct_menu_skipping_much_lesson(tr_days):
    """
    Make a menu when one day contains two or more lessons for skipping
    """
    buttons = []
    row = []
    date_info = tr_days.first().date
    for tr_day in tr_days:
        time_tlg, _, _, _, _, _, _ = get_time_info_from_tr_day(tr_day)
        row.append(
            inlinebutt(
                f'{time_tlg}', callback_data="{}{}".format(SELECT_SKIP_TIME_BUTTON, tr_day.id))
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        inlinebutt(BACK_BUTTON,
                   callback_data=create_callback_data(CLNDR_ACTION_SKIP, CLNDR_ACTION_BACK, date_info.year,
                                                      date_info.month, 0))
    ])

    return inlinemark(buttons)


def construct_detail_menu_for_skipping(training_day, purpose, group_name, group_players):
    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(training_day)
    text = f'<b>{date_tlg} ({day_of_week})\n{time_tlg}\n</b>' + group_name + '\n' + group_players

    buttons = [[
        InlineKeyboardButton('Пропустить', callback_data=SHOW_INFO_ABOUT_SKIPPING_DAY + f'{training_day.id}')
    ], [
        InlineKeyboardButton(BACK_BUTTON,
                             callback_data=create_callback_data(purpose, CLNDR_ACTION_BACK, training_day.date.year,
                                                                training_day.date.month, 0))
    ]]
    return InlineKeyboardMarkup(buttons), text
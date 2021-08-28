import datetime
from datetime import datetime, timedelta
from typing import List

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from base.common_for_bots.utils import DT_BOT_FORMAT, TM_TIME_SCHEDULE_FORMAT, get_time_info_from_tr_day, \
    create_callback_data
from player_bot.take_lesson import manage_data
from player_bot.calendar.manage_data import CLNDR_ACTION_TAKE_GROUP, CLNDR_ACTION_TAKE_IND
from base.common_for_bots.manage_data import CLNDR_DAY, CLNDR_ACTION_BACK
from player_bot.take_lesson.static_text import TAKE_LESSON_BUTTON
from base.common_for_bots.static_text import BACK_BUTTON


def ind_group_type_training_keyboard():
    buttons = [[
        InlineKeyboardButton('Индивидуальная',
                             callback_data=f"{manage_data.SELECT_TRAINING_TYPE}{manage_data.TRAINING_IND}")
    ], [
        InlineKeyboardButton('Групповая',
                             callback_data=f"{manage_data.SELECT_TRAINING_TYPE}{manage_data.TRAINING_GROUP}")
    ]]

    return InlineKeyboardMarkup(buttons)


def ind_train_choose_duration_keyboard():
    buttons = [[
        InlineKeyboardButton('1 час', callback_data=manage_data.SELECT_DURATION_FOR_IND_TRAIN + '1.0')
    ], [
        InlineKeyboardButton('1.5 часа', callback_data=manage_data.SELECT_DURATION_FOR_IND_TRAIN + '1.5')
    ], [
        InlineKeyboardButton('2 часа', callback_data=manage_data.SELECT_DURATION_FOR_IND_TRAIN + '2.0')
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}', callback_data=TAKE_LESSON_BUTTON),
    ]]

    return InlineKeyboardMarkup(buttons)


def take_lesson_back_keyboard(tr_day_id, year, month, day):
    buttons = [[
        InlineKeyboardButton('Записаться', callback_data=f"{manage_data.CONFIRM_GROUP_LESSON}{tr_day_id}")
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=create_callback_data(CLNDR_ACTION_TAKE_GROUP, CLNDR_DAY, year, month, day))
    ]]

    return InlineKeyboardMarkup(buttons)


def choose_type_of_payment_for_group_lesson_keyboard(payment_add_lesson, tr_day_id, tarif):
    buttons = [[
        InlineKeyboardButton(
            f'За отыгрыш + {payment_add_lesson}₽',
            callback_data=f"{manage_data.PAYMENT_VISITING}{manage_data.PAYMENT_MONEY_AND_BONUS_LESSONS}|{tr_day_id}")
    ], [
        InlineKeyboardButton(f'За {tarif}₽',
                             callback_data=f"{manage_data.PAYMENT_VISITING}{manage_data.PAYMENT_MONEY}|{tr_day_id}")
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=f"{manage_data.SELECT_PRECISE_GROUP_TIME}{tr_day_id}")
    ]]
    return InlineKeyboardMarkup(buttons)


def back_to_group_times_when_no_left_keyboard(year, month, day):
    """
        Создает клавиатура с кнопкой назад, когда в данном
        тренировочном дне на выбранное время уже нет
        свободных мест
    """
    buttons = [[
        InlineKeyboardButton(
            f'{BACK_BUTTON}',
            callback_data=create_callback_data(
                purpose=CLNDR_ACTION_TAKE_GROUP,
                action=CLNDR_DAY,
                year=year,
                month=month,
                day=day
            )
        )
    ]]
    return InlineKeyboardMarkup(buttons)


def construct_time_menu_for_group_lesson(button_text, tr_days, date, purpose):
    buttons = []
    row = []
    for day in tr_days:
        time_tlg, _, _, _, _, _, _ = get_time_info_from_tr_day(day)
        row.append(
            InlineKeyboardButton(f'{time_tlg}', callback_data=button_text + str(day.id))
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=create_callback_data(purpose, CLNDR_ACTION_BACK, date.year, date.month, 0)),
    ])

    return InlineKeyboardMarkup(buttons)


def construct_time_menu_4ind_and_rent_lesson(
        button_text: str, poss_training_times: List[datetime.time], day_date: datetime.date, duration: float
) -> InlineKeyboardMarkup:
    buttons = []
    row = []
    for start_time in poss_training_times:
        end_time = datetime.combine(day_date, start_time) + timedelta(hours=duration)
        row.append(
            InlineKeyboardButton(
                text=f'{start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}',
                callback_data=f"{button_text}{day_date.strftime(DT_BOT_FORMAT)}|{start_time}|{end_time.time()}"
            )
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        InlineKeyboardButton(
            text=f'{BACK_BUTTON}',
            callback_data=create_callback_data(
                f'{CLNDR_ACTION_TAKE_IND}{duration}', CLNDR_ACTION_BACK, day_date.year, day_date.month, 0
            )
        )
    ])
    return InlineKeyboardMarkup(buttons)

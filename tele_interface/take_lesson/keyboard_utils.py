import datetime
from datetime import datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton as inlinebutt, \
    InlineKeyboardMarkup as inlinemark
from base.utils import get_time_info_from_tr_day, TM_TIME_SCHEDULE_FORMAT, DT_BOT_FORMAT
from tele_interface.manage_data import SELECT_TRAINING_TYPE, SELECT_DURATION_FOR_IND_TRAIN, CONFIRM_GROUP_LESSON, \
    CLNDR_ACTION_TAKE_GROUP, CLNDR_DAY, PAYMENT_VISITING, PAYMENT_MONEY_AND_BONUS_LESSONS, PAYMENT_MONEY, SELECT_PRECISE_GROUP_TIME, \
    CLNDR_ACTION_BACK, CLNDR_ACTION_TAKE_IND
from tele_interface.static_text import BACK_BUTTON, TAKE_LESSON_BUTTON
from tele_interface.utils import create_callback_data


def ind_group_type_training_keyboard():
    buttons = [[
        InlineKeyboardButton('Индивидуальная', callback_data=SELECT_TRAINING_TYPE + 'ind')
    ], [
        InlineKeyboardButton('Групповая', callback_data=SELECT_TRAINING_TYPE + 'group')
    ]]

    return InlineKeyboardMarkup(buttons)


def ind_train_choose_duration_keyboard():
    buttons = [[
        InlineKeyboardButton('1 час', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.0')
    ], [
        InlineKeyboardButton('1.5 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.5')
    ], [
        InlineKeyboardButton('2 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '2.0')
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}', callback_data=TAKE_LESSON_BUTTON),
    ]]

    return InlineKeyboardMarkup(buttons)


def take_lesson_back_keyboard(tr_day_id, year, month, day):
    buttons = [[
        InlineKeyboardButton('Записаться', callback_data=f"{CONFIRM_GROUP_LESSON}{tr_day_id}")
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}',
                      callback_data=create_callback_data(CLNDR_ACTION_TAKE_GROUP, CLNDR_DAY, year, month, day))
    ]]

    return InlineKeyboardMarkup(buttons)


def choose_type_of_payment_for_group_lesson_keyboard(payment_add_lesson, tr_day_id, tarif):
    buttons = [[
        InlineKeyboardButton(f'За отыгрыш + {payment_add_lesson}₽',
                             callback_data=f"{PAYMENT_VISITING}{PAYMENT_MONEY_AND_BONUS_LESSONS}|{tr_day_id}")
    ], [
        InlineKeyboardButton(f'За {tarif}₽',
                      callback_data=f"{PAYMENT_VISITING}{PAYMENT_MONEY}|{tr_day_id}")
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}',
                      callback_data=f"{SELECT_PRECISE_GROUP_TIME}{tr_day_id}")
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
            InlineKeyboardButton(f'{time_tlg}',
                                 callback_data=button_text + str(day.id))
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


def construct_time_menu_4ind_lesson(button_text, poss_training_times: list, day: datetime.date, duration: float, user):
    buttons = []
    row = []
    for start_time in poss_training_times:

        end_time = datetime.combine(day, start_time) + timedelta(hours=duration)
        row.append(
            inlinebutt(f'{start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}',
                       callback_data=f"{button_text}{day.strftime(DT_BOT_FORMAT)}|{start_time}|{end_time.time()}")
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        inlinebutt(f'{BACK_BUTTON}',
                   callback_data=create_callback_data(f'{CLNDR_ACTION_TAKE_IND}{duration}', CLNDR_ACTION_BACK, day.year,
                                                      day.month, 0))
    ])

    return inlinemark(buttons)
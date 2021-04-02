import calendar
import datetime
from datetime import date, datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton as inlinebutt, \
    InlineKeyboardMarkup as inlinemark

from base.utils import moscow_datetime, get_time_info_from_tr_day, TM_TIME_SCHEDULE_FORMAT, DT_BOT_FORMAT
from tele_interface.manage_data import CLNDR_IGNORE, CLNDR_DAY, CLNDR_PREV_MONTH, CLNDR_NEXT_MONTH, CLNDR_ACTION_BACK, \
    SHOW_INFO_ABOUT_SKIPPING_DAY, SELECT_SKIP_TIME_BUTTON, CLNDR_ACTION_SKIP, CLNDR_ACTION_TAKE_IND, \
    CLNDR_ACTION_TAKE_GROUP, \
    PAYMENT_VISITING, PAYMENT_BONUS, PAYMENT_MONEY, SELECT_PRECISE_GROUP_TIME, CONFIRM_GROUP_LESSON, \
    SELECT_DURATION_FOR_IND_TRAIN, SELECT_TRAINING_TYPE
from tele_interface.static_text import from_digit_to_month, BACK_BUTTON, TAKE_LESSON_BUTTON
from tele_interface.utils import create_callback_data


def create_calendar(purpose_of_calendar, year=None, month=None, dates_to_highlight=None):
    """
    Create an inline keyboard with the provided year and month
    :param list of dates dates_to_highlight : date we should highlight, e.g. days available for skipping
    :param str purpose_of_calendar: e.g. skipping, taking lesson
    :param int year: Year to use in the calendar, if None the current year is used.
    :param int month: Month to use in the calendar, if None the current month is used.
    :return: Returns the InlineKeyboardMarkup object with the calendar.
    """
    now = moscow_datetime(datetime.now())
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    data_ignore = create_callback_data(purpose_of_calendar, CLNDR_IGNORE, year, month, 0)
    keyboard = []
    # First row - Month and Year
    row = [InlineKeyboardButton(from_digit_to_month[month] + " " + str(year), callback_data=data_ignore)]
    keyboard.append(row)
    # Second row - Week Days
    row = []
    for day in ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:

            if day == 0:
                row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
            else:
                day_info = str(day)
                if dates_to_highlight and (date(year, month, day) in dates_to_highlight):
                    day_info = f'{str(day)}✅'
                row.append(InlineKeyboardButton(day_info, callback_data=create_callback_data(purpose_of_calendar,
                                                                                             CLNDR_DAY, year, month,
                                                                                             day)))
        keyboard.append(row)
    # Last row - Buttons
    row = [InlineKeyboardButton("<", callback_data=create_callback_data(purpose_of_calendar, CLNDR_PREV_MONTH, year,
                                                                        month, day)),
           InlineKeyboardButton(" ", callback_data=data_ignore),
           InlineKeyboardButton(">", callback_data=create_callback_data(purpose_of_calendar, CLNDR_NEXT_MONTH, year,
                                                                        month, day))]
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


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


def construct_detail_menu_for_skipping(training_day, purpose, group_name, group_players):
    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(training_day)
    text = f'<b>{date_tlg} ({day_of_week})\n{time_tlg}\n</b>' + group_name + '\n' + group_players

    buttons = [[
        InlineKeyboardButton('Пропустить', callback_data=SHOW_INFO_ABOUT_SKIPPING_DAY + f'{training_day.id}')
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=create_callback_data(purpose, CLNDR_ACTION_BACK, training_day.date.year,
                                                                training_day.date.month, 0))
    ]]
    return InlineKeyboardMarkup(buttons), text


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
        inlinebutt(f'{BACK_BUTTON}',
                   callback_data=create_callback_data(CLNDR_ACTION_SKIP, CLNDR_ACTION_BACK, date_info.year,
                                                      date_info.month, 0))
    ])

    return inlinemark(buttons)


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


def back_to_group_times_when_no_left_keyboard(year, month, day):
    """
        Создает клавиатура с кнопкой назад, когда в данном
        тренировочном дне на выбранное время уже нет
        свободных мест
    """
    buttons = [[
        InlineKeyboardButton(f'{BACK_BUTTON}',
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


def back_to_group_when_trying_to_enter_his_own_group(tr_day_id):
    buttons = [[
        InlineKeyboardButton(f'{BACK_BUTTON}',
                      callback_data=SELECT_PRECISE_GROUP_TIME + f'{tr_day_id}')
    ]]
    return InlineKeyboardMarkup(buttons)



def choose_type_of_payment_for_group_lesson_keyboard(payment_add_lesson, tr_day_id, tarif):
    buttons = [[
        InlineKeyboardButton(f'За отыгрыш + {payment_add_lesson}₽',
                      callback_data=f"{PAYMENT_VISITING}{PAYMENT_BONUS}|{tr_day_id}")
    ], [
        InlineKeyboardButton(f'За {tarif}₽',
                      callback_data=f"{PAYMENT_VISITING}{PAYMENT_MONEY}|{tr_day_id}")
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}',
                      callback_data=f"{SELECT_PRECISE_GROUP_TIME}{tr_day_id}")
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


def ind_train_choose_duration_keyboard():
    buttons = [[
        InlineKeyboardButton('1 час', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.0')
    ], [
        InlineKeyboardButton('1.5 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '1.5')
    ], [
        InlineKeyboardButton('2 часа', callback_data=SELECT_DURATION_FOR_IND_TRAIN + '2.0')
    ], [
        InlineKeyboardButton(f'{BACK_BUTTON}',
                      callback_data=TAKE_LESSON_BUTTON),
    ]]

    return InlineKeyboardMarkup(buttons)


def ind_group_type_training_keyboard():
    buttons = [[
        InlineKeyboardButton('Индивидуальная', callback_data=SELECT_TRAINING_TYPE + 'ind')
    ], [
        InlineKeyboardButton('Групповая', callback_data=SELECT_TRAINING_TYPE + 'group')
    ]]

    return InlineKeyboardMarkup(buttons)


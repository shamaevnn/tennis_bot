import calendar
import datetime
from collections import Counter
from datetime import date, datetime, timedelta

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton as inlinebutt, \
    InlineKeyboardMarkup as inlinemark, ReplyKeyboardMarkup

from base.utils import moscow_datetime, get_time_info_from_tr_day, TM_TIME_SCHEDULE_FORMAT, DT_BOT_FORMAT
from tele_interface.manage_data import CLNDR_IGNORE, CLNDR_DAY, CLNDR_PREV_MONTH, CLNDR_NEXT_MONTH, CLNDR_ACTION_BACK, \
    SHOW_INFO_ABOUT_SKIPPING_DAY, SELECT_SKIP_TIME_BUTTON, CLNDR_ACTION_SKIP, CLNDR_ACTION_TAKE_IND, \
    CLNDR_ADMIN_VIEW_SCHEDULE, PAYMENT_YEAR_MONTH_GROUP, PAYMENT_YEAR, SEND_MESSAGE
from tele_interface.static_text import from_digit_to_month, BACK_BUTTON, ADMIN_PAYMENT, ADMIN_TIME_SCHEDULE_BUTTON, \
    ADMIN_SITE, ADMIN_SEND_MESSAGE
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


def day_buttons_coach_info(tr_days, button_text):
    buttons = []
    row = []
    for day in tr_days:
        time_tlg, _, _, _, _, _, _ = get_time_info_from_tr_day(day)
        row.append(
            inlinebutt(f'{day.group.name}', callback_data=f"{button_text}{day.id}")
        )
        row.append(
            inlinebutt(
                f'{time_tlg}',
                callback_data=f"{button_text}{day.id}")
        )
        if len(row) >= 2:
            buttons.append(row)
            row = []
    if len(row):
        buttons.append(row)

    buttons.append([
        inlinebutt(f'{BACK_BUTTON}',
                   callback_data=create_callback_data(CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, tr_days.first().date.year, tr_days.first().date.month, 0)),
    ])

    return inlinemark(buttons)


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

    buttons.append([InlineKeyboardButton('Оставшиеся', callback_data=f'{button_text}{0}')])

    year, month, _ = button_text[len(PAYMENT_YEAR_MONTH_GROUP):].split('|')
    buttons.append([
        InlineKeyboardButton(f'{BACK_BUTTON}',
                             callback_data=f'{PAYMENT_YEAR}{year}'),
    ])

    return InlineKeyboardMarkup(buttons)


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

    if '0' not in group_ids:
        all_groups_text = 'Всем группам'
    elif ids_counter['0'] > 1 and ids_counter['0'] % 2 == 0:
        all_groups_text = 'Всем группам'
        group_ids.remove('0')
        group_ids.remove('0')
        button_text = button_text[:len(SEND_MESSAGE)] + "|".join(group_ids)
    else:
        all_groups_text = 'Всем группам ✅'

    buttons.append([InlineKeyboardButton(all_groups_text, callback_data=f'{button_text}|{0}')])
    buttons.append([InlineKeyboardButton('Подтвердить', callback_data=f'{button_text}|{-1}')])

    return InlineKeyboardMarkup(buttons)


def construct_admin_main_menu():
    return ReplyKeyboardMarkup([
        [ADMIN_PAYMENT, ADMIN_TIME_SCHEDULE_BUTTON],
        [ADMIN_SITE, ADMIN_SEND_MESSAGE]],
        resize_keyboard=True)
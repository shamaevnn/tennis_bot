from base.models import User, Payment
from functools import wraps
from collections import Counter

from base.utils import get_time_info_from_tr_day
from tele_interface.manage_data import CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, BACK_BUTTON, ADMIN_PAYMENT, \
    PAYMENT_YEAR_MONTH_GROUP, PAYMENT_YEAR, SEND_MESSAGE, ADMIN_TIME_SCHEDULE_BUTTON, ADMIN_SITE, ADMIN_SEND_MESSAGE
from tele_interface.utils import create_callback_data
from tennis_bot.settings import DEBUG
from telegram import (InlineKeyboardButton as inlinebutt,
                      InlineKeyboardMarkup as inlinemark, InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup, )

import sys
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def admin_handler_decor():
    """
    декоратор для всех handlers в телеграм боте
    :return:
    """

    def decor(func):
        @wraps(func)
        def wrapper(bot, update):

            if DEBUG:
                logger.info(str(update) + '\n {}'.format(func.__name__))

            if update.callback_query:
                user_details = update.callback_query.from_user
            elif update.inline_query:
                user_details = update.inline_query.from_user
            else:
                user_details = update.message.from_user

            user = User.objects.get(id=user_details.id)
            res = None
            if user.is_staff:
                try:
                    res = func(bot, update, user)
                except Exception as e:
                    msg = f'{e}\n\nчто-то пошло не так, напиши @ta2asho'
                    res = [bot.send_message(user.id, msg)]
                    tb = sys.exc_info()[2]
                    raise e.with_traceback(tb)
            else:
                bot.send_message(
                    user.id,
                    "Привет! я переехал на @TennisTula_bot",
                    parse_mode='HTML',
                )
            return res
        return wrapper
    return decor


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


def check_if_players_not_in_payments(group_id, payments, year, month):
    payment_user_ids = list(payments.values_list('player_id', flat=True))
    users_not_in_payments = User.objects.filter(traininggroup__id=group_id).exclude(id__in=payment_user_ids)
    if users_not_in_payments.count():
        for player in users_not_in_payments:
            Payment.objects.create(player=player, month=month, year=year)


def construct_admin_main_menu():
    return ReplyKeyboardMarkup([
        [ADMIN_PAYMENT, ADMIN_TIME_SCHEDULE_BUTTON],
        [ADMIN_SITE, ADMIN_SEND_MESSAGE]],
        resize_keyboard=True)
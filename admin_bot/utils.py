from base.models import User
from functools import wraps

from base.utils import  TM_TIME_SCHEDULE_FORMAT
from tele_interface.manage_data import CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, BACK_BUTTON
from tele_interface.utils import create_callback_data
from tennis_bot.settings import DEBUG
from telegram import (InlineKeyboardButton as inlinebutt,
                      InlineKeyboardMarkup as inlinemark,)

import datetime
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

        end_time = datetime.datetime.combine(day.date,
                                             day.start_time) + day.duration

        row.append(
            inlinebutt(f'{day.group.name}', callback_data=f"{button_text}{day.id}")
        )
        row.append(
            inlinebutt(
                f'{day.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)} — {end_time.strftime(TM_TIME_SCHEDULE_FORMAT)}',
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

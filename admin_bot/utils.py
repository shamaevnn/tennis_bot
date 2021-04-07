from base.models import User, Payment
from functools import wraps

from tennis_bot.settings import DEBUG

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


def check_if_players_not_in_payments(group_id, payments, year, month):
    payment_user_ids = list(payments.values_list('player_id', flat=True))
    users_not_in_payments = User.objects.filter(traininggroup__id=group_id).exclude(id__in=payment_user_ids)
    if users_not_in_payments.exists():
        for player in users_not_in_payments:
            Payment.objects.create(player=player, month=month, year=year)



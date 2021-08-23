import time
from typing import List

import telegram
from celery.utils.log import get_task_logger
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from base.models import User
from tennis_bot.celery import app
from tennis_bot.settings import TELEGRAM_TOKEN, DEBUG

logger = get_task_logger(__name__)


def send_message(user_id: int, text: str, reply_markup=None, tg_token=TELEGRAM_TOKEN, parse_mode='HTML'):
    bot = telegram.Bot(tg_token)
    try:
        if not DEBUG:
            if reply_markup is not None:
                if reply_markup.get('inline_keyboard'):
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(**button)
                                                          for button in reply_markup.get('inline_keyboard')[0]]])

        m = bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )
    except telegram.error.Unauthorized:
        print(f"Can't send message to {user_id}. Reason: Bot was stopped.")
        User.objects.filter(id=user_id).update(is_blocked=True)
        success = False
    except Exception as e:
        print(f"Can't send message to {user_id}. Reason: {e}")
        success = False
    else:
        success = True
        User.objects.filter(id=user_id).update(is_blocked=False)
    return success


@app.task(ignore_result=True)
def broadcast_message(
        user_ids: List[int],
        message: str,
        reply_markup=None,
        tg_token=TELEGRAM_TOKEN,
        sleep_between=0.4,
        parse_mode="HTML"
):
    """ It's used to broadcast message to big amount of users """
    logger.info(f"Going to send message: '{message}' to {len(user_ids)} users")

    for user_id in user_ids:
        try:
            send_message(
                user_id=user_id,
                text=message,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                tg_token=tg_token,
            )
            logger.info(f"Broadcast message was sent to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}, reason: {e}" )
        time.sleep(max(sleep_between, 0.1))

    logger.info("Broadcast finished!")


def clear_broadcast_messages(
        user_ids: List[int],
        message: str,
        reply_markup=None,
        tg_token=TELEGRAM_TOKEN,
        sleep_between=0.4,
        parse_mode="HTML"
):
    if DEBUG:
        broadcast_message(
            user_ids=user_ids,
            message=message,
            reply_markup=reply_markup,
            tg_token=tg_token,
            sleep_between=sleep_between,
            parse_mode=parse_mode
        )
    else:
        broadcast_message.delay(
            user_ids=user_ids,
            message=message,
            reply_markup=reply_markup.to_dict() if reply_markup else None,
            tg_token=tg_token,
            sleep_between=sleep_between,
            parse_mode=parse_mode
        )



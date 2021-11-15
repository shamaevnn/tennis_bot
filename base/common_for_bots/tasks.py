import time
from typing import List

import telegram
from celery.utils.log import get_task_logger
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from base.models import Player
from tennis_bot.celery import app
from tennis_bot.settings import TELEGRAM_TOKEN, DEBUG

logger = get_task_logger(__name__)


def send_message(chat_id: int, text: str, reply_markup=None, tg_token=TELEGRAM_TOKEN, parse_mode='HTML'):
    bot = telegram.Bot(tg_token)
    try:
        if not DEBUG:
            if reply_markup is not None:
                if reply_markup.get('inline_keyboard'):
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(**button)
                                                          for button in reply_markup.get('inline_keyboard')[0]]])

        m = bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )
    except telegram.error.Unauthorized:
        print(f"Can't send message to {chat_id}. Reason: Bot was stopped.")
        Player.objects.filter(tg_id=chat_id).update(has_blocked_bot=True)
        success = False
    except Exception as e:
        print(f"Can't send message to {chat_id}. Reason: {e}")
        success = False
    else:
        success = True
        Player.objects.filter(tg_id=chat_id).update(has_blocked_bot=False)
    return success


@app.task(ignore_result=True)
def broadcast_message(
        chat_ids: List[int],
        message: str,
        reply_markup=None,
        tg_token=TELEGRAM_TOKEN,
        sleep_between=0.4,
        parse_mode="HTML"
):
    """ It's used to broadcast message to big amount of users """
    logger.info(f"Going to send message: '{message}' to {len(chat_ids)} users")

    for chat_id in chat_ids:
        try:
            send_message(
                chat_id=chat_id,
                text=message,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                tg_token=tg_token,
            )
            logger.info(f"Broadcast message was sent to {chat_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {chat_id}, reason: {e}")
        time.sleep(max(sleep_between, 0.1))

    logger.info("Broadcast finished!")


def clear_broadcast_messages(
        chat_ids: List[int],
        message: str,
        reply_markup=None,
        tg_token=TELEGRAM_TOKEN,
        sleep_between=0.4,
        parse_mode="HTML"
):
    if DEBUG:
        broadcast_message(
            chat_ids=chat_ids,
            message=message,
            reply_markup=reply_markup,
            tg_token=tg_token,
            sleep_between=sleep_between,
            parse_mode=parse_mode
        )
    else:
        broadcast_message.delay(
            chat_ids=chat_ids,
            message=message,
            reply_markup=reply_markup.to_dict() if reply_markup else None,
            tg_token=tg_token,
            sleep_between=sleep_between,
            parse_mode=parse_mode
        )



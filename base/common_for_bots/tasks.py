import time

from base.common_for_bots.utils import send_message
from base.tasks import logger
from tennis_bot.celery import app
from tennis_bot.settings import TELEGRAM_TOKEN


@app.task(ignore_result=True)
def broadcast_message(user_ids, message, reply_markup=None, tg_token=TELEGRAM_TOKEN, sleep_between=0.4, parse_mode="HTML"):
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
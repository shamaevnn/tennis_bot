import logging
import traceback
import html

from telegram import Update, ParseMode
from telegram.ext import CallbackContext

from base.models import Player
from player_bot.errors.static_text import SOMETHING_WENT_WRONG_DONT_WORRY
from tennis_bot.settings import ADMIN_CHAT_ID


def send_stacktrace_to_tg_chat(update: Update, context: CallbackContext) -> None:
    player = Player.from_update(update)

    logging.error("Exception while handling an update:", exc_info=context.error)

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    context.bot.send_message(
        chat_id=player.tg_id,
        text=SOMETHING_WENT_WRONG_DONT_WORRY,
    )

    message = f"<pre>{html.escape(tb_string)}</pre>"
    admin_message = f"⚠️⚠️⚠️ for <a href='{player.get_link_to_django_admin}'>{player.tg_name}</a>:\n{message}"[
        :4090
    ]
    if ADMIN_CHAT_ID:
        context.bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message,
            parse_mode=ParseMode.HTML,
        )
    else:
        logging.error(admin_message)

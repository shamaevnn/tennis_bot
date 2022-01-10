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

    # отправляем сообщение пользователю о том, чтобы он не волновался, что админы знают об ошибке
    context.bot.send_message(
        chat_id=player.tg_id,
        text=SOMETHING_WENT_WRONG_DONT_WORRY,
    )

    tb_list = traceback.format_exception(
        None, context.error, context.error.__traceback__
    )
    tb_string = "".join(tb_list)
    error_message = f"<pre>{html.escape(tb_string)}</pre>"

    if "telegram.error.BadRequest: Message is not modified" in error_message:
        return

    admin_message = f"⚠️⚠️⚠️ for <a href='{player.get_link_to_django_admin}'>{player.tg_name}</a>:\n{error_message}"[
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

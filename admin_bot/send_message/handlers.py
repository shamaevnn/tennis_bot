from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from .keyboards import construct_menu_groups_for_send_message
from admin_bot.send_message import static_text
from base.common_for_bots.static_text import UP_TO_YOU
from base.models import TrainingGroup
from base.common_for_bots.utils import bot_edit_message
from base.common_for_bots.tasks import broadcast_messages
from .manage_data import SEND_MESSAGE, CONFIRM_SENDING
from .utils import get_text_and_player_ids_to_send_message_to

GROUP_IDS, TEXT_TO_SEND = 2, 3


def select_groups_where_should_send(update: Update, context: CallbackContext):
    text = static_text.WHOM_TO_SEND_TO

    banda_groups = TrainingGroup.get_banda_groups()
    if update.callback_query:
        group_ids = update.callback_query.data[len(SEND_MESSAGE) :].split("|")
        markup = construct_menu_groups_for_send_message(
            banda_groups, f"{update.callback_query.data}"
        )

        if len(group_ids) == 2 and group_ids[-1] == "-1":
            # ['', '-1'] — just pressed confirm
            text = static_text.CHOOSE_GROUP_AFTER_THAT_CONFIRM
        bot_edit_message(context.bot, text, update, markup)
        return GROUP_IDS
    else:
        markup = construct_menu_groups_for_send_message(banda_groups, f"{SEND_MESSAGE}")
        update.message.reply_text(text=text, reply_markup=markup)


def text_to_send(update: Update, context: CallbackContext):
    group_ids = update.callback_query.data[len(SEND_MESSAGE) :].split("|")
    group_ids.remove("")

    if group_ids[-1] != CONFIRM_SENDING:
        select_groups_where_should_send(update, context)
        return

    # pressed "confirm"
    text, player_ids = get_text_and_player_ids_to_send_message_to(group_ids=group_ids)
    text += static_text.OR_PRESS_CANCEL

    context.user_data["player_ids"] = player_ids
    bot_edit_message(context.bot, text, update)
    return TEXT_TO_SEND


def receive_text_and_send(update: Update, context: CallbackContext):
    text = update.message.text

    if text == static_text.CANCEL_COMMAND:
        update.message.reply_text(text=UP_TO_YOU)
    else:
        player_ids = context.user_data["player_ids"]
        broadcast_messages(chat_ids=player_ids, message=text)
        update.message.reply_text(text=static_text.IS_SENT)

    del context.user_data["player_ids"]
    return ConversationHandler.END

from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from .static_text import OK_CREATED_CHILD, CHILDREN_REG_FIO
from base.models import Player
from ..children_info.keyboards import list_all_children_with_add_one_more_button

INSERT_CHILD_FIO = range(1)


def insert_child_first_last_name(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=CHILDREN_REG_FIO)
    return INSERT_CHILD_FIO


def get_child_first_last_name_and_create_child(update: Update, context: CallbackContext):
    text = update.message.text
    last_name, first_name = text.split(' ')

    parent = Player.from_update(update)
    parent.create_child(first_name=first_name, last_name=last_name)

    update.message.reply_text(
        text=OK_CREATED_CHILD.format(first_name=first_name, last_name=last_name),
        reply_markup=list_all_children_with_add_one_more_button(parent)
    )
    return ConversationHandler.END

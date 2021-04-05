from telegram.ext import ConversationHandler

from admin_bot.keyboard_utils import construct_admin_main_menu
from admin_bot.static_text import HEY_I_MOVED_TO, THIS_WAY_YEAH


def start(update, context):
    update.message.reply_text(
        HEY_I_MOVED_TO,
        parse_mode='HTML',
        reply_markup=construct_admin_main_menu(),
    )


def cancel(update, context):
    update.message.reply_text(THIS_WAY_YEAH,
                              reply_markup=construct_admin_main_menu())

    return ConversationHandler.END
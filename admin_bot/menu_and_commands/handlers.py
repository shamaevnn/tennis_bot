from telegram.ext import ConversationHandler

from admin_bot.menu_and_commands.keyboard_utils import construct_admin_main_menu
from admin_bot.menu_and_commands.static_text import HEY_I_MOVED_TO
from base.common_for_bots.static_text import THIS_WAY_YEAH


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
from telegram import ParseMode, Update
from telegram.ext import ConversationHandler, CallbackContext

from admin_bot.menu_and_commands.keyboards import construct_admin_main_menu
from admin_bot.menu_and_commands.static_text import HEY_I_MOVED_TO
from base.common_for_bots.static_text import THIS_WAY_YEAH


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=HEY_I_MOVED_TO,
        parse_mode=ParseMode.HTML,
        reply_markup=construct_admin_main_menu(),
    )
    return


def cancel(update: Update, context: CallbackContext):
    update.message.reply_text(
        text=THIS_WAY_YEAH, reply_markup=construct_admin_main_menu()
    )
    return ConversationHandler.END

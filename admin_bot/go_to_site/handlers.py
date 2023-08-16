from telegram import Update
from telegram.ext import CallbackContext

from admin_bot.go_to_site.keyboards import go_to_site_keyboard
from admin_bot.go_to_site.static_text import ADMIN_SITE
from admin_bot.menu_and_commands.utils import check_coach_status_decor


@check_coach_status_decor
def redirect_to_site(update: Update, context: CallbackContext):
    markup = go_to_site_keyboard()
    update.message.reply_text(text=ADMIN_SITE, reply_markup=markup)

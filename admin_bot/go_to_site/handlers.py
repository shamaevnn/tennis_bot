from telegram import Update

from admin_bot.go_to_site.keyboards import go_to_site_keyboard
from admin_bot.go_to_site.static_text import ADMIN_SITE


def redirect_to_site(update: Update, context):
    markup = go_to_site_keyboard()
    update.message.reply_text(
        text=ADMIN_SITE,
        reply_markup=markup
    )

from telegram import ReplyKeyboardMarkup

from admin_bot.go_to_site.static_text import ADMIN_SITE
from admin_bot.payment.static_text import ADMIN_PAYMENT
from admin_bot.send_message.static_text import ADMIN_SEND_MESSAGE
from admin_bot.view_schedule.static_text import ADMIN_TIME_SCHEDULE_BUTTON


def construct_admin_main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [ADMIN_PAYMENT, ADMIN_TIME_SCHEDULE_BUTTON],
            [ADMIN_SITE, ADMIN_SEND_MESSAGE],
        ],
        resize_keyboard=True,
    )

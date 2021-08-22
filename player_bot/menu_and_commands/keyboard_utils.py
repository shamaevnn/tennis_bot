from datetime import date
from typing import Optional

from telegram import ReplyKeyboardMarkup

from base.models import User, Payment
from player_bot.take_lesson.static_text import TAKE_LESSON_BUTTON
from player_bot.skip_lesson.static_text import SKIP_LESSON_BUTTON
from player_bot.menu_and_commands.static_text import HELP_BUTTON
from player_bot.user_info.static_text import MY_DATA_BUTTON, NO_PAYMENT_BUTTON


def construct_main_menu(user: Optional[User] = None):
    payment_button = []
    if user and user.status == User.STATUS_TRAINING:
        today_date = date.today()
        user_payment = Payment.objects.filter(player=user, player__status=user.status, fact_amount=0,
                                              year=today_date.year-2020, month=today_date.month)
        if user_payment.exists():
            payment_button = [NO_PAYMENT_BUTTON]

    return ReplyKeyboardMarkup(
        [
            payment_button,
            [MY_DATA_BUTTON, HELP_BUTTON],
            [SKIP_LESSON_BUTTON, TAKE_LESSON_BUTTON]
        ],
        resize_keyboard=True
    )

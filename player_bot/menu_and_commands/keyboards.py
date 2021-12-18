from datetime import date
from typing import Optional

from telegram import ReplyKeyboardMarkup

from base.models import Payment, Player
from player_bot.take_lesson.static_text import TAKE_LESSON_BUTTON
from player_bot.skip_lesson.static_text import SKIP_LESSON_BUTTON
from player_bot.menu_and_commands.static_text import HELP_BUTTON
from player_bot.player_info.static_text import MY_DATA_BUTTON, NO_PAYMENT_BUTTON


def construct_main_menu(player: Optional[Player] = None):
    payment_button = []
    if player and player.status == Player.STATUS_TRAINING:
        today_date = date.today()
        player_payment = Payment.objects.filter(
            player=player,
            player__status=player.status,
            fact_amount=0,
            year=today_date.year - 2020,
            month=today_date.month,
        )
        if player_payment.exists():
            payment_button = [NO_PAYMENT_BUTTON]

    return ReplyKeyboardMarkup(
        [
            payment_button,
            [MY_DATA_BUTTON, HELP_BUTTON],
            [SKIP_LESSON_BUTTON, TAKE_LESSON_BUTTON],
        ],
        resize_keyboard=True,
    )

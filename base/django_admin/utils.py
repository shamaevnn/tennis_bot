from django.db.models import F

from base.common_for_bots.utils import get_actual_players_without_absent, get_players_for_tr_day
from base.common_for_bots.tasks import clear_broadcast_messages
from player_bot.menu_and_commands.keyboards import construct_main_menu
from base.django_admin.static_text import CANCEL_TRAIN_PLUS_BONUS_LESSON_2, TRAIN_IS_AVAILABLE_CONGRATS


def send_alert_about_changing_tr_day_status(tr_day, new_is_available):
    if not new_is_available:
        text = CANCEL_TRAIN_PLUS_BONUS_LESSON_2.format(tr_day.date, tr_day.start_time)
        users = get_actual_players_without_absent(tr_day)
        users.update(bonus_lesson=F('bonus_lesson') + 1)
    else:
        text = TRAIN_IS_AVAILABLE_CONGRATS.format(tr_day.date, tr_day.start_time)

    clear_broadcast_messages(
        user_ids=list(get_players_for_tr_day(tr_day).values_list('id', flat=True)),
        message=text,
        reply_markup=construct_main_menu()
    )


def send_alert_about_changing_tr_day_time(tr_day, text):
    absents = tr_day.absent.all()
    clear_broadcast_messages(
        user_ids=list(get_players_for_tr_day(tr_day).union(absents).values_list('id', flat=True)),
        message=text,
        reply_markup=construct_main_menu()
    )

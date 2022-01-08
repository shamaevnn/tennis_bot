from django.db.models import F

from base.common_for_bots.utils import (
    get_actual_players_without_absent,
    get_players_for_tr_day, get_dttm_info_for_tr_day,
)
from base.common_for_bots.tasks import broadcast_messages
from base.models import GroupTrainingDay, Player
from player_bot.menu_and_commands.keyboards import construct_main_menu
from base.django_admin.static_text import (
    CANCEL_TRAIN_PLUS_BONUS_LESSON_2,
    TRAIN_IS_AVAILABLE_CONGRATS,
)


def send_alert_about_changing_tr_day_status(tr_day: GroupTrainingDay, new_is_available: bool):
    date_info = get_dttm_info_for_tr_day(tr_day=tr_day)

    if not new_is_available:
        text = CANCEL_TRAIN_PLUS_BONUS_LESSON_2.format(date_info=date_info)
        players = get_actual_players_without_absent(tr_day)
        player_ids = players.values("id")
        Player.objects.filter(id__in=player_ids).update(
            bonus_lesson=F("bonus_lesson") + 1
        )
    else:
        text = TRAIN_IS_AVAILABLE_CONGRATS.format(date_info=date_info)

    broadcast_messages(
        chat_ids=list(get_players_for_tr_day(tr_day).values_list("id", flat=True)),
        message=text,
        reply_markup=construct_main_menu(),
    )


def send_alert_about_changing_tr_day_time(tr_day: GroupTrainingDay, text: str):
    absents = tr_day.absent.all()
    broadcast_messages(
        chat_ids=list(
            get_players_for_tr_day(tr_day).union(absents).values_list("id", flat=True)
        ),
        message=text,
        reply_markup=construct_main_menu(),
    )

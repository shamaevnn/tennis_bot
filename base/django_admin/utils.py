from django.db.models import F

from base.common_for_bots.utils import (
    get_actual_players_without_absent,
    get_players_for_tr_day,
    get_dttm_info_for_tr_day,
)
from base.common_for_bots.tasks import broadcast_messages
from base.models import GroupTrainingDay, Player, TrainingGroup
from player_bot.menu_and_commands.keyboards import construct_main_menu
from base.django_admin.static_text import (
    CANCEL_TRAIN_PLUS_BONUS_LESSON_2,
    TRAIN_IS_AVAILABLE_CONGRATS,
)
from base.utils.change_available_status import (
    change_tr_day_available_status,
    get_text_about_the_available_status_change,
)


def send_alert_about_changing_tr_day_time(tr_day: GroupTrainingDay, text: str):
    absents = tr_day.absent.all()
    broadcast_messages(
        chat_ids=list(
            get_players_for_tr_day(tr_day)
            .union(absents)
            .values_list("tg_id", flat=True)
        ),
        message=text,
        reply_markup=construct_main_menu(),
    )

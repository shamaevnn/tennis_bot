from telegram import Update, Bot, ParseMode
from telegram.ext import CallbackContext

from player_bot.take_lesson.rent.static_text import (
    COACH_ACCEPTED_RENT_COURT,
    COACH_CANCELLED_RENT_COURT,
)
from tennis_bot.settings import TELEGRAM_TOKEN
from .manage_data import PERMISSION_FOR_RENT_COURT, PERMISSION_YES
from .static_text import (
    WILL_SAY_RENT_COURT_IS_CANCELLED,
    RENT_COURT_IS_ALREADY_CANCELLED,
    WILL_SAY_RENT_IS_ACCEPTED,
)
from base.common_for_bots.static_text import DATE_INFO, ATTENTION
from base.common_for_bots.utils import get_time_info_from_tr_day, bot_edit_message
from base.models import GroupTrainingDay, Player


def permission_for_rent_court(update: Update, context: CallbackContext):
    permission, tg_id, tr_day_id = update.callback_query.data[
        len(PERMISSION_FOR_RENT_COURT) :
    ].split("|")

    player = Player.objects.get(tg_id=tg_id)
    tr_day = GroupTrainingDay.objects.filter(id=tr_day_id)

    if tr_day.exists():
        tr_day = tr_day.first()
        time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
        date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)
        markup = None

        if permission == PERMISSION_YES:
            player_text = COACH_ACCEPTED_RENT_COURT.format(date_info=date_info)
            admin_text = WILL_SAY_RENT_IS_ACCEPTED.format(
                last_name=player.last_name,
                first_name=player.first_name,
                date_info=date_info,
            )
        else:
            admin_text = WILL_SAY_RENT_COURT_IS_CANCELLED.format(
                last_name=player.last_name,
                first_name=player.first_name,
                date_info=date_info,
            )
            player_text = COACH_CANCELLED_RENT_COURT.format(
                attention=ATTENTION, date_info=date_info
            )
            tr_day.is_deleted = True
            tr_day.save()

        tennis_bot = Bot(TELEGRAM_TOKEN)
        tennis_bot.send_message(
            chat_id=player.tg_id, text=player_text, parse_mode=ParseMode.HTML
        )
    else:
        admin_text = RENT_COURT_IS_ALREADY_CANCELLED
        markup = None

    bot_edit_message(context.bot, admin_text, update, markup=markup)

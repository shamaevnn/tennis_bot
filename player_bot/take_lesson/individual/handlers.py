import calendar
from datetime import datetime

from telegram import Update
from telegram.ext import CallbackContext

from admin_bot.ind_train.keyboards import permission4ind_train_keyboard
from base.common_for_bots.static_text import from_eng_to_rus_day_week
from base.common_for_bots.tasks import send_message_to_coaches
from base.common_for_bots.utils import create_calendar, bot_edit_message, DT_BOT_FORMAT
from base.models import Player, TrainingGroup, GroupTrainingDay
from player_bot.calendar.manage_data import CLNDR_ACTION_TAKE_IND
from player_bot.take_lesson.individual import manage_data
from player_bot.take_lesson.individual.static_text import (
    PLAYER_WANTS_IND_TRAIN,
    WILL_SAY_TO_COACH_ABOUT_IND_TRAIN,
)
from player_bot.take_lesson.static_text import CHOOSE_DATE_OF_TRAIN


def select_dt_for_ind_lesson(update: Update, context: CallbackContext):
    duration = float(
        update.callback_query.data[len(manage_data.SELECT_DURATION_FOR_IND_TRAIN) :]
    )
    markup = create_calendar(f"{CLNDR_ACTION_TAKE_IND}{duration}")
    bot_edit_message(context.bot, CHOOSE_DATE_OF_TRAIN, update, markup)


def select_ind_time(update: Update, context: CallbackContext):
    day_dt, start_time, end_time = update.callback_query.data[
        len(manage_data.SELECT_PRECISE_IND_TIME) :
    ].split("|")
    date_dt = datetime.strptime(day_dt, DT_BOT_FORMAT)
    st_time_obj = datetime.strptime(start_time, "%H:%M:%S")
    end_time_obj = datetime.strptime(end_time, "%H:%M:%S")
    duration = end_time_obj - st_time_obj

    day_of_week = from_eng_to_rus_day_week[calendar.day_name[date_dt.date().weekday()]]

    player = Player.from_update(update)
    group = TrainingGroup.get_or_create_ind_group(player)

    tr_day = GroupTrainingDay.objects.create(
        group=group,
        date=date_dt,
        start_time=st_time_obj,
        duration=duration,
        status=GroupTrainingDay.INDIVIDUAL_TRAIN,
    )

    text = WILL_SAY_TO_COACH_ABOUT_IND_TRAIN.format(
        day_dt, day_of_week, start_time, end_time
    )

    bot_edit_message(context.bot, text, update)

    markup = permission4ind_train_keyboard(
        tg_id=player.tg_id,
        tr_day_id=tr_day.id,
    )

    text = PLAYER_WANTS_IND_TRAIN.format(
        player.first_name,
        player.last_name,
        player.phone_number,
        day_dt,
        day_of_week,
        start_time,
        end_time,
    )

    send_message_to_coaches(
        text=text,
        reply_markup=markup,
    )

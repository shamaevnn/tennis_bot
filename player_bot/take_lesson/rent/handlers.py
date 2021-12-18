import calendar
from datetime import datetime, timedelta

from telegram import Update
from telegram.ext import CallbackContext

from admin_bot.rent_court.keyboards import permission4rent_keyboard
from admin_bot.rent_court.static_text import PLAYER_WANTS_TO_RENT_COURT
from base.common_for_bots.static_text import from_eng_to_rus_day_week, DATE_INFO
from base.common_for_bots.tasks import send_message_to_coaches
from base.common_for_bots.utils import (
    create_calendar,
    bot_edit_message,
    DT_BOT_FORMAT,
    get_time_info_from_tr_day,
)
from base.models import Player, TrainingGroup, GroupTrainingDay
from . import manage_data
from .keyboards import number_of_people_to_rent_cort_keyboard, take_rent_lesson_or_back
from .manage_data import NUMBER_OF_PEOPLE_TO_RENT_CORT, TAKE_RENT_LESSON
from .static_text import (
    HOW_MANY_PEOPLE_WILL_COME,
    TRAIN_RENT_INFO,
    WILL_SAY_TO_COACH_ABOUT_RENTING,
)
from .utils import _get_price_for_renting
from ..static_text import CHOOSE_DATE_OF_TRAIN
from ...calendar.manage_data import CLNDR_ACTION_TAKE_RENT


def select_dt_for_rent_lesson(update: Update, context: CallbackContext):
    duration = float(
        update.callback_query.data[len(manage_data.SELECT_DURATION_FOR_RENT) :]
    )
    markup = create_calendar(f"{CLNDR_ACTION_TAKE_RENT}{duration}")
    bot_edit_message(context.bot, CHOOSE_DATE_OF_TRAIN, update, markup)


def select_rent_time(update: Update, context: CallbackContext):
    """
    После того, как выбрал точное время, дату и продолжительность, спрашиваем, сколько придет человек.
    """

    # day_dt, start_time, end_time = update.callback_query.data[len(manage_data.SELECT_PRECISE_RENT_TIME):].split('|')
    training_time_data: str = update.callback_query.data[
        len(manage_data.SELECT_PRECISE_RENT_TIME) :
    ]
    day_dt, start_time, end_time = training_time_data.split("|")

    date_dt: datetime = datetime.strptime(day_dt, DT_BOT_FORMAT)
    st_time_obj: datetime = datetime.strptime(start_time, "%H:%M:%S")
    end_time_obj: datetime = datetime.strptime(end_time, "%H:%M:%S")
    duration: timedelta = end_time_obj - st_time_obj
    duration_hours: float = duration.seconds / 3600

    markup = number_of_people_to_rent_cort_keyboard(
        training_time_data, duration_hours, date_dt
    )
    bot_edit_message(context.bot, HOW_MANY_PEOPLE_WILL_COME, update, markup)


def take_rent_info_train(update: Update, context: CallbackContext):
    """
    После выбора всех параметров аренды, показываем краткую инфу + кнопку записаться
    """

    player_number_training_time_data: str = update.callback_query.data[
        len(NUMBER_OF_PEOPLE_TO_RENT_CORT) :
    ]

    # 6 2021.10.31 18:30:00 20:00:00
    (
        number_of_players,
        day_dt,
        start_time,
        end_time,
    ) = player_number_training_time_data.split("|")

    date_dt: datetime = datetime.strptime(day_dt, DT_BOT_FORMAT)
    day_of_week: str = from_eng_to_rus_day_week[
        calendar.day_name[date_dt.date().weekday()]
    ]
    st_time_obj: datetime = datetime.strptime(start_time, "%H:%M:%S")
    end_time_obj: datetime = datetime.strptime(end_time, "%H:%M:%S")
    duration: timedelta = end_time_obj - st_time_obj
    duration_hours: float = duration.seconds / 3600

    price_for_renting = _get_price_for_renting(number_of_players, duration_hours)

    text = TRAIN_RENT_INFO.format(
        n_players=number_of_players,
        price=price_for_renting,
        date=day_dt,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
    )
    markup = take_rent_lesson_or_back(
        number_of_players=number_of_players,
        training_time_data="|".join((day_dt, start_time, end_time)),
    )
    bot_edit_message(context.bot, text, update, markup)


def take_rent(update: Update, context: CallbackContext):
    """
    Игрок окончательно подтвердил, что хочет арендовать корт.
    """
    player_number_training_time_data: str = update.callback_query.data[
        len(TAKE_RENT_LESSON) :
    ]
    (
        number_of_players,
        day_dt,
        start_time,
        end_time,
    ) = player_number_training_time_data.split("|")

    date_dt: datetime = datetime.strptime(day_dt, DT_BOT_FORMAT)
    st_time_obj: datetime = datetime.strptime(start_time, "%H:%M:%S")
    end_time_obj: datetime = datetime.strptime(end_time, "%H:%M:%S")
    duration: timedelta = end_time_obj - st_time_obj
    duration_hours: float = duration.seconds / 3600

    price_for_renting = _get_price_for_renting(number_of_players, duration_hours)

    player = Player.from_update(update)
    group = TrainingGroup.get_or_create_rent_group(player)
    tr_day = GroupTrainingDay.objects.create(
        group=group,
        date=date_dt,
        start_time=st_time_obj.time(),
        duration=duration,
        tr_day_status=GroupTrainingDay.RENT_COURT_STATUS,
    )
    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    text = WILL_SAY_TO_COACH_ABOUT_RENTING.format(
        price=price_for_renting,
        n_players=number_of_players,
        date=day_dt,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
    )
    bot_edit_message(context.bot, text, update)

    markup = permission4rent_keyboard(
        tg_id=player.tg_id,
        tr_day_id=tr_day.id,
    )

    admin_text = PLAYER_WANTS_TO_RENT_COURT.format(
        first_name=player.first_name,
        last_name=player.last_name,
        phone_number=player.phone_number,
        n_players=number_of_players,
        price=price_for_renting,
        date_info=date_info,
    )

    send_message_to_coaches(
        text=admin_text,
        reply_markup=markup,
    )

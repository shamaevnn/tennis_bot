import calendar
from datetime import datetime

from admin_bot.ind_train.keyboards import permission4ind_train_keyboard
from base.common_for_bots.static_text import from_eng_to_rus_day_week
from base.common_for_bots.tasks import clear_broadcast_messages, send_message_to_coaches
from base.common_for_bots.utils import create_calendar, bot_edit_message, DT_BOT_FORMAT
from base.models import Player, TrainingGroup, GroupTrainingDay
from player_bot.calendar.manage_data import CLNDR_ACTION_TAKE_IND
from player_bot.take_lesson.individual import manage_data
from player_bot.take_lesson.static_text import CHOOSE_DATE_OF_TRAIN
from tennis_bot.settings import ADMIN_TELEGRAM_TOKEN


def select_dt_for_ind_lesson(update, context):
    duration = float(update.callback_query.data[len(manage_data.SELECT_DURATION_FOR_IND_TRAIN):])
    markup = create_calendar(f'{CLNDR_ACTION_TAKE_IND}{duration}')
    bot_edit_message(context.bot, CHOOSE_DATE_OF_TRAIN, update, markup)


def select_ind_time(update, context):
    day_dt, start_time, end_time = update.callback_query.data[len(manage_data.SELECT_PRECISE_IND_TIME):].split('|')
    date_dt = datetime.strptime(day_dt, DT_BOT_FORMAT)
    st_time_obj = datetime.strptime(start_time, '%H:%M:%S')
    end_time_obj = datetime.strptime(end_time, '%H:%M:%S')
    duration = end_time_obj - st_time_obj

    day_of_week = from_eng_to_rus_day_week[calendar.day_name[date_dt.date().weekday()]]

    player = Player.from_update(update)
    group = TrainingGroup.get_or_create_ind_group(player)

    tr_day = GroupTrainingDay.objects.create(group=group, date=date_dt, start_time=st_time_obj, duration=duration,
                                             is_individual=True)

    text = f"Сообщу тренеру, что ты хочешь прийти на индивидуальное занятие"\
           f" <b>{day_dt} ({day_of_week}) </b>\n"\
           f"Время: <b>{start_time} — {end_time}</b>"
    bot_edit_message(context.bot, text, update)

    markup = permission4ind_train_keyboard(
        tg_id=player.tg_id,
        tr_day_id=tr_day.id,
    )

    text = f"<b>{player.first_name} {player.last_name} — {player.phone_number}</b>\n" \
           f"Хочет прийти на индивидуальное занятие <b>{day_dt} ({day_of_week}) </b>" \
           f" в <b>{start_time} — {end_time}</b>\n" \
           f"<b>Разрешить?</b>"

    send_message_to_coaches(
        text=text,
        reply_markup=markup,
    )

import re
from datetime import datetime, date, time
from typing import List, Dict, Generator, Tuple

from django.db.models import QuerySet
from telegram import InlineKeyboardMarkup

from base.models import GroupTrainingDay
from base.common_for_bots.utils import TM_TIME_SCHEDULE_FORMAT, create_calendar
from player_bot.take_lesson.keyboards import construct_time_menu_4ind_and_rent_lesson
from player_bot.take_lesson.static_text import (
    CANT_TAKE_TRAIN_CHOOSE_ANOTHER_DAY,
    CHOOSE_TIME,
)


def calendar_taking_rent_and_ind_lesson(
    calendar_action: str,
    button_data: str,
    purpose: str,
    date_time: datetime,
) -> Tuple[str, InlineKeyboardMarkup]:
    duration = re.findall(rf"({calendar_action})(\d.\d)", purpose)[0][1]
    date_comparison = date(date_time.year, date_time.month, date_time.day)
    possible_start_time_for_period = list(
        get_available_start_times_for_given_duration_and_date(duration, date_comparison)
    )

    if date_comparison < date.today():
        text = CANT_TAKE_TRAIN_CHOOSE_ANOTHER_DAY
        markup = create_calendar(purpose, date_time.year, date_time.month)
        return text, markup

    if len(possible_start_time_for_period):
        markup = construct_time_menu_4ind_and_rent_lesson(
            button_data,
            possible_start_time_for_period,
            date_comparison,
            float(duration),
            calendar_action,
        )
        text = CHOOSE_TIME
    else:
        text = CANT_TAKE_TRAIN_CHOOSE_ANOTHER_DAY
        markup = create_calendar(purpose, date_time.year, date_time.month)
    return text, markup


def get_available_start_times_for_given_duration_and_date(
    duration_in_hours: str, tr_day_date: datetime.date
) -> Generator[time, None, None]:
    # в первом цикле определяем те часы:минуты, в которые не может начаться занятие.
    # если занятие идет с 13:30 до 15:30, то туда попадет 13:30, 14:00, 14:30, 15:00
    # (делается это во внутреннем цикле)

    # втором цикле идем по каждым 30 минутам, начиная с 8:00. если данное время уже в первом списке, то идем дальше.
    # В ином случае нужно проверить (внутренний цикл), что для данного периода следующие несколько 30 минут
    # не в первом списке. Если они все не попадают туда, то заносим в итоговый список с возможным стартовым временем.
    start_hour = 8
    end_hour = 20

    exist_tr_days: QuerySet[Dict] = (
        GroupTrainingDay.objects.filter(
            is_available=True,
            is_deleted=False,
            date=tr_day_date,
        )
        .values("start_time", "duration")
        .order_by("start_time")
        .iterator()
    )

    banned_start_time: List[str] = []
    from_time_to_str_time = lambda time_instance: time_instance.strftime(
        TM_TIME_SCHEDULE_FORMAT
    )
    # первый цикл
    for x in exist_tr_days:
        start_minutes = x["start_time"].hour * 60 + x["start_time"].minute
        end_minutes = int(start_minutes + x["duration"].seconds / 60)
        for minute in range(start_minutes, end_minutes, 30):
            banned_start_time.append(
                from_time_to_str_time(time(minute // 60, minute % 60))
            )

    from_minutes_to_time = lambda minutes: time(hour=minutes // 60, minute=minutes % 60)
    # второй цикл

    for hour_minute in range(start_hour * 60, end_hour * 60 + 1, 30):
        # занятия могут идти с 8 до 20 с интервалом 30 минут
        time_ = from_minutes_to_time(hour_minute)
        str_time = from_time_to_str_time(time_)
        if time_ >= time(20, 0) and int(float(duration_in_hours) * 60) > 60:
            # нельзя, чтобы тренировка была после 21:00
            continue

        if str_time in banned_start_time:
            continue
        else:
            # нет занятия, которое начинается в это время
            for minute_duration in range(
                30, int(float(duration_in_hours) * 60) - 1, 30
            ):
                if (
                    from_time_to_str_time(
                        from_minutes_to_time(hour_minute + minute_duration)
                    )
                    in banned_start_time
                ):
                    break
            else:
                yield time_

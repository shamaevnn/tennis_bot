import calendar

from datetime import date, datetime
from typing import Tuple

from telegram import InlineKeyboardMarkup

from base.common_for_bots.static_text import from_eng_to_rus_day_week
from base.common_for_bots.utils import DT_BOT_FORMAT, create_calendar
from base.models import Player
from player_bot.take_lesson.group.keyboards import construct_time_menu_for_group_lesson
from player_bot.take_lesson.group.manage_data import SELECT_PRECISE_GROUP_TIME
from player_bot.take_lesson.group.query import get_potential_days_for_group_training

from .static_text import (
    CHOOSE_TRAIN_TIME_TEMPLATE, NO_AVAILABLE_TRAIN_THIS_DAY
    )


def calendar_taking_group_lesson(
    player: Player, purpose: str, date_time: datetime
) -> Tuple[str, InlineKeyboardMarkup]:
    """
    Игрок выбирает конкретный день из календаря.
    Если в этот день есть доступные тренировки, предлагается выбрать конкретное время
    Иначе предлагается выбрать другой день в календаре
    """
    date_comparison = date(date_time.year, date_time.month, date_time.day)
    trainings_this_day = get_potential_days_for_group_training(player, date=date_comparison)
    if trainings_this_day.exists():
        markup = construct_time_menu_for_group_lesson(
            SELECT_PRECISE_GROUP_TIME, trainings_this_day, date_time, purpose
        )

        day_of_week = calendar.day_name[date_time.weekday()]
        rus_week_day = from_eng_to_rus_day_week[day_of_week]
        string_formatted_date = date_time.strftime(DT_BOT_FORMAT)
        text = CHOOSE_TRAIN_TIME_TEMPLATE.format(string_formatted_date, rus_week_day)
    else:
        text = NO_AVAILABLE_TRAIN_THIS_DAY 
        trainings = get_potential_days_for_group_training(player)
        highlight_dates = list(trainings.values_list("date", flat=True))
        markup = create_calendar(
            purpose, date_time.year, date_time.month, highlight_dates
        )
    return text, markup

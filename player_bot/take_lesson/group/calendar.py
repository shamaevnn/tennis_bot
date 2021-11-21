import calendar

from datetime import date
from base.common_for_bots.static_text import from_eng_to_rus_day_week
from base.common_for_bots.utils import DT_BOT_FORMAT, create_calendar
from base.models import Player
from player_bot.take_lesson.group.keyboards import construct_time_menu_for_group_lesson
from player_bot.take_lesson.group.manage_data import SELECT_PRECISE_GROUP_TIME
from player_bot.take_lesson.group.query import get_potential_days_for_group_training


def calendar_taking_group_lesson(player: Player, purpose, date_time):
    date_comparison = date(date_time.year, date_time.month, date_time.day)
    training_days = get_potential_days_for_group_training(player, date=date_comparison)
    highlight_dates = list(training_days.values_list('date', flat=True))
    if training_days.exists():
        buttons = construct_time_menu_for_group_lesson(SELECT_PRECISE_GROUP_TIME, training_days, date_time,
                                                       purpose)

        day_of_week = calendar.day_name[date_time.weekday()]
        text = f'Выбери время занятия на {date_time.strftime(DT_BOT_FORMAT)} ({from_eng_to_rus_day_week[day_of_week]}).'
        markup = buttons
    else:
        text = 'Нет доступных тренировок в этот день, выбери другой.\n' \
               '✅ -- дни, доступные для групповых тренировок'
        markup = create_calendar(purpose, date_time.year, date_time.month, highlight_dates)
    return text, markup

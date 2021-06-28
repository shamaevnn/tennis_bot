import datetime
import re
from calendar import calendar
from datetime import timedelta, datetime, time

from django.db.models import Count, F, ExpressionWrapper, DurationField, Q, DateTimeField
from django.db.models.functions import TruncDate

from base.models import GroupTrainingDay, TrainingGroup
from base.utils import moscow_datetime, DT_BOT_FORMAT
from tele_interface.keyboard_utils import construct_time_menu_for_group_lesson, create_calendar, \
    construct_time_menu_4ind_lesson
from tele_interface.manage_data import SELECT_PRECISE_GROUP_TIME, CLNDR_ACTION_TAKE_IND, SELECT_PRECISE_IND_TIME
from tele_interface.static_text import from_eng_to_rus_day_week


def get_potential_days_for_group_training(user, **filters):
    potential_free_places = GroupTrainingDay.objects.tr_day_is_my_available(
        group__status=TrainingGroup.STATUS_GROUP,
        is_individual=False
    ).annotate(
        Count('absent', distinct=True),
        Count('group__users', distinct=True),
        Count('visitors', distinct=True),
        Count('pay_visitors', distinct=True),
        Count('pay_bonus_visitors', distinct=True),
        max_players=F('group__max_players'),
        diff=ExpressionWrapper(
            F('start_time') + F('date') - moscow_datetime(datetime.now()),
            output_field=DurationField()
        )
    ).annotate(
        all_users=F('pay_visitors__count') + F('visitors__count') + F('pay_bonus_visitors__count') +
                  F('group__users__count') - F('absent__count')
    ).filter(
        Q(max_players__gt=F('all_users')) |
        (
                Q(max_players__lte=F('all_users')) &
                Q(group__available_for_additional_lessons=True) &
                Q(max_players__lt=6) &
                Q(all_users__lt=6)
        ),
        diff__gte=timedelta(microseconds=5),
        max_players__gt=1,
        **filters
    ).exclude(
        Q(visitors__in=[user]) |
        Q(group__users__in=[user]) |
        Q(pay_visitors__in=[user]) |
        Q(pay_bonus_visitors__in=[user])
    ).order_by('start_time')

    return potential_free_places


def calendar_taking_lesson(user, purpose, date_my, date_comparison):
    training_days = get_potential_days_for_group_training(user, date=date_comparison)
    highlight_dates = list(training_days.values_list('date', flat=True))
    if training_days.exists():
        buttons = construct_time_menu_for_group_lesson(SELECT_PRECISE_GROUP_TIME, training_days, date_my,
                                                       purpose)

        day_of_week = calendar.day_name[date_my.weekday()]
        text = f'Выбери время занятия на {date_my.strftime(DT_BOT_FORMAT)} ({from_eng_to_rus_day_week[day_of_week]}).'
        markup = buttons
    else:
        text = 'Нет доступных тренировок в этот день, выбери другой.\n' \
               '✅ -- дни, доступные для групповых тренировок'
        markup = create_calendar(purpose, date_my.year, date_my.month, highlight_dates)
    return text, markup


def generate_times_to_remove(start_time: time, end_time: time):
    times_to_remove = []
    start = start_time
    while start < end_time:
        if start.minute == 0:
            start = time(start.hour, 30)
        elif start.minute == 30:
            hour = start.hour + 1
            start = time(hour, 0)
        times_to_remove.append(start)
    del times_to_remove[-1]
    return times_to_remove


def get_available_dt_time4ind_train(duration: float, tr_day_date=moscow_datetime(datetime.now()).date()):
    # todo: какой-то пиздец, без пол литра не разберешься, хз шо с этим делать
    poss_date = moscow_datetime(datetime.now()).date()
    start_time = time(8, 0, 0)

    exist_tr_days = GroupTrainingDay.objects.tr_day_is_my_available(
        date=tr_day_date,
        start_time__gte=start_time
    ).annotate(
        end_time=ExpressionWrapper(
            F('start_time') + F('duration'), output_field=DateTimeField()
        ),
        date_tmp=TruncDate('date')
    ).values('date_tmp', 'start_time', 'end_time').order_by('date', 'start_time')

    possible_times = []
    for i in range(8, 21):  # занятия могут идти с 8 до 20
        for minute in [0, 30]:  # с интервалом 30 минут
            possible_times.append(time(i, minute))
    del possible_times[-1]
    poss_date_time_dict = {day['date_tmp']: possible_times[:] for day in exist_tr_days}

    if exist_tr_days.count():
        for day in exist_tr_days:
            times_to_remove = generate_times_to_remove(day['start_time'], day['end_time'])
            for x in times_to_remove:
                if x in poss_date_time_dict[day['date_tmp']]:
                    poss_date_time_dict[day['date_tmp']].remove(x)

    else:
        if not tr_day_date in poss_date_time_dict:
            poss_date_time_dict[tr_day_date] = possible_times[:]
            if tr_day_date == poss_date:
                now_time = moscow_datetime(datetime.now()).time()
                if now_time < start_time:
                    times_to_remove = []
                else:
                    times_to_remove = generate_times_to_remove(time(8, 0, 0), now_time)
            else:
                times_to_remove = []
            for x in times_to_remove:
                if x in poss_date_time_dict[tr_day_date]:
                    poss_date_time_dict[tr_day_date].remove(x)

    poss_date_for_train = []
    for poss_date in poss_date_time_dict:
        for i in range(len(poss_date_time_dict[poss_date]) - int(duration * 2)):
            if datetime.combine(poss_date, poss_date_time_dict[poss_date][i + int(duration * 2)]) - datetime.combine(
                    poss_date, poss_date_time_dict[poss_date][i]) == timedelta(hours=duration):
                poss_date_for_train.append(poss_date)

    return poss_date_time_dict


def calendar_taking_ind_lesson(user, purpose, date_my, date_comparison):
    duration = re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose)[0][1]
    date_time_dict = get_available_dt_time4ind_train(float(duration), date_comparison)

    poss_time_for_train = []
    if date_time_dict.get(date_comparison):
        for i in range(len(date_time_dict[date_comparison]) - int(float(duration) * 2)):
            if datetime.combine(date_comparison, date_time_dict[date_comparison][
                i + int(float(duration) * 2)]) - datetime.combine(
                date_comparison, date_time_dict[date_comparison][i]) == timedelta(hours=float(duration)):
                poss_time_for_train.append(date_time_dict[date_comparison][i])

        markup = construct_time_menu_4ind_lesson(SELECT_PRECISE_IND_TIME, poss_time_for_train,
                                                 date_comparison,
                                                 float(duration), user)
        text = 'Выбери время'
    else:
        text = 'Нельзя записаться на этот день, выбери другой.'
        markup = create_calendar(purpose, date_my.year, date_my.month)
    return text, markup



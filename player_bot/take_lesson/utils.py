import datetime
import re
import calendar
from datetime import timedelta, datetime, time
from typing import List, Dict

from django.db.models import Count, F, ExpressionWrapper, DurationField, Q

from base.common_for_bots.static_text import DATE_INFO, from_eng_to_rus_day_week
from base.models import GroupTrainingDay, TrainingGroup, User
from base.common_for_bots.utils import DT_BOT_FORMAT, get_n_free_places, moscow_datetime, get_time_info_from_tr_day, \
    create_calendar, TM_TIME_SCHEDULE_FORMAT
from player_bot.take_lesson.keyboard_utils import construct_time_menu_for_group_lesson, \
    construct_time_menu_4ind_and_rent_lesson, choose_type_of_payment_for_group_lesson_keyboard, \
    back_to_group_times_when_no_left_keyboard
from player_bot.take_lesson.manage_data import SELECT_PRECISE_GROUP_TIME, SELECT_PRECISE_IND_TIME, \
    PAYMENT_MONEY_AND_BONUS_LESSONS, PAYMENT_MONEY
from player_bot.calendar.manage_data import CLNDR_ACTION_TAKE_IND
from player_bot.take_lesson.static_text import NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER, CHOOSE_TYPE_OF_PAYMENT
from tennis_bot.settings import TARIF_ARBITRARY, TARIF_GROUP, TARIF_PAYMENT_ADD_LESSON


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


def get_available_start_times_for_given_duration_and_date(
        duration_in_hours: str, tr_day_date: datetime.date
) -> List[time]:
    # в первом цикле определяем те часы:минуты, в которые не может начаться занятие.
    # если занятие идет с 13:30 до 15:30, то туда попадет 13:30, 14:00, 14:30, 15:00
    # (делается это во внутреннем цикле)

    # втором цикле идем по каждым 30 минутам, начиная с 8:00. если данное время уже в первом списке, то идем дальше.
    # В ином случае нужно проверить (внутренний цикл), что для данного периода следующие несколько 30 минут
    # не в первом списке. Если они все не попадают туда, то заносим в итоговый список с возможным стартовым временем.
    start_hour = 8
    end_hour = 20

    exist_tr_days: Dict = GroupTrainingDay.objects.tr_day_is_my_available(
        date=tr_day_date
    ).values('start_time', 'duration').order_by('start_time')

    banned_start_time: List[str] = []
    from_time_to_str_time = lambda time_instance: time_instance.strftime(TM_TIME_SCHEDULE_FORMAT)
    # первый цикл
    for x in exist_tr_days:
        start_minutes = x['start_time'].hour * 60 + x['start_time'].minute
        end_minutes = int(start_minutes + x['duration'].seconds / 60)
        for minute in range(start_minutes, end_minutes, 30):
            banned_start_time.append(from_time_to_str_time(time(minute // 60, minute % 60)))

    possible_start_times_for_given_period: List[time] = []
    from_minutes_to_time = lambda minutes: time(hour=minutes // 60, minute=minutes % 60)
    # второй цикл
    for hour_minute in range(start_hour * 60, end_hour * 60 + 1, 30):  # занятия могут идти с 8 до 20 с интервалом 30 минут
        time_ = from_minutes_to_time(hour_minute)
        str_time = from_time_to_str_time(time_)
        if time_ >= time(20, 0) and int(float(duration_in_hours) * 60) > 60:
            continue
        if str_time in banned_start_time:
            continue
        else:
            # нет занятия, которое начинается в это время
            for minute_duration in range(30, int(float(duration_in_hours) * 60) - 1, 30):
                if from_time_to_str_time(from_minutes_to_time(hour_minute + minute_duration)) in banned_start_time:
                    break
            else:
                possible_start_times_for_given_period.append(time_)
    return possible_start_times_for_given_period


def calendar_taking_ind_lesson(purpose, date_my, date_comparison):
    duration = re.findall(rf'({CLNDR_ACTION_TAKE_IND})(\d.\d)', purpose)[0][1]
    possible_start_time_for_period = get_available_start_times_for_given_duration_and_date(duration, date_comparison)

    if len(possible_start_time_for_period):
        markup = construct_time_menu_4ind_and_rent_lesson(
            SELECT_PRECISE_IND_TIME, possible_start_time_for_period, date_comparison, float(duration)
        )
        text = 'Выбери время'
    else:
        text = 'Нельзя записаться на этот день, выбери другой.'
        markup = create_calendar(purpose, date_my.year, date_my.month)
    return text, markup


def handle_taking_group_lesson(user: User, tr_day: GroupTrainingDay):
    time_tlg, _, _, date_tlg, day_of_week, _, end_time = get_time_info_from_tr_day(tr_day)
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    n_free_places = get_n_free_places(tr_day)

    admin_text = ''
    admin_markup = None
    if n_free_places > 0:
        tr_day.visitors.add(user)
        user_text = f'Записал тебя на тренировку.\n{date_info}'
        user_markup = None

        if user.bonus_lesson > 0 and user.status == User.STATUS_TRAINING:
            admin_text = f'{user.first_name} {user.last_name} придёт на гр. тренировку за отыгрыш.\n{date_info}'
            user.bonus_lesson -= 1
            user.save()
        else:
            admin_text = f'⚠️ATTENTION⚠️\n' \
                         f'{user.first_name} {user.last_name} придёт на гр. тренировку ' \
                         f'<b>не за счет отыгрышей, не забудь взять {TARIF_ARBITRARY}₽.</b>\n' \
                         f'{date_info}'
    else:
        if tr_day.group.available_for_additional_lessons and tr_day.group.max_players < 6:
            tarif = TARIF_ARBITRARY if user.status == User.STATUS_ARBITRARY else TARIF_GROUP
            if user.bonus_lesson == 0:
                tr_day.pay_visitors.add(user)
                user_text = f'Записал тебя на тренировку' \
                            f'⚠️ATTENTION⚠️\n' \
                            f'Не забудь заплатить <b>{tarif}₽</b>\n' \
                            f'{date_info}'
                admin_text = f'⚠️ATTENTION⚠️\n' \
                             f'{user.first_name} {user.last_name} придёт на гр. тренировку ' \
                             f'<b>не за счет отыгрышей, не забудь взять {tarif}₽.</b>\n' \
                             f'{date_info}'
                user_markup = None
            else:
                user_text = CHOOSE_TYPE_OF_PAYMENT
                user_markup = choose_type_of_payment_for_group_lesson_keyboard(
                    payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                    tr_day_id=tr_day.id,
                    tarif=tarif,
                )
        else:
            user_text = NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER
            user_markup = back_to_group_times_when_no_left_keyboard(
                year=tr_day.date.year,
                month=tr_day.date.month,
                day=tr_day.date.day
            )

    return user_text, user_markup, admin_text, admin_markup


def handle_choosing_type_of_payment_for_pay_visiting_when_have_bonus_lessons(
        user: User, tr_day: GroupTrainingDay, payment_choice: str
):
    # todo: tests on this function
    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

    user_text, admin_text = '', ''
    if payment_choice == PAYMENT_MONEY_AND_BONUS_LESSONS:
        user.bonus_lesson -= 1
        user.save()

        tr_day.pay_bonus_visitors.add(user)
        user_text = f'Записал тебя на тренировку\n' \
                    f'⚠️ATTENTION⚠️\n' \
                    f'Не забудь заплатить <b>{TARIF_PAYMENT_ADD_LESSON}₽</b>\n{date_info}'

        admin_text = f'⚠️ATTENTION⚠️\n' \
                     f'{user.first_name} {user.last_name} придёт ' \
                     f'<b>за счёт платных отыгрышей, не забудь взять {TARIF_PAYMENT_ADD_LESSON}₽.</b>\n{date_info}'

    elif payment_choice == PAYMENT_MONEY:
        tr_day.pay_visitors.add(user)
        tarif = TARIF_ARBITRARY if user.status == User.STATUS_ARBITRARY else TARIF_GROUP

        user_text = f'Записал тебя на тренировку\n' \
                    f'⚠️ATTENTION⚠️\n' \
                    f'Не забудь заплатить <b>{tarif}₽</b>\n{date_info}'

        admin_text = f'⚠️ATTENTION⚠️\n' \
                     f'{user.first_name} {user.last_name} придёт ' \
                     f'<b>в дополнительное время, не забудь взять {tarif}₽.</b>\n{date_info}'

    return user_text, admin_text

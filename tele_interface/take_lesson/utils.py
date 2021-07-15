import datetime
import re
import calendar
from datetime import timedelta, datetime, time

from django.db.models import Count, F, ExpressionWrapper, DurationField, Q, DateTimeField
from django.db.models.functions import TruncDate

from admin_bot.static_text import DATE_INFO
from base.models import GroupTrainingDay, TrainingGroup, User
from base.utils import moscow_datetime, DT_BOT_FORMAT, get_time_info_from_tr_day, get_n_free_places
from tele_interface.keyboard_utils import create_calendar
from tele_interface.take_lesson.keyboard_utils import construct_time_menu_for_group_lesson, \
    construct_time_menu_4ind_lesson, choose_type_of_payment_for_group_lesson_keyboard, \
    back_to_group_times_when_no_left_keyboard
from tele_interface.manage_data import SELECT_PRECISE_GROUP_TIME, CLNDR_ACTION_TAKE_IND, SELECT_PRECISE_IND_TIME, \
    PAYMENT_MONEY_AND_BONUS_LESSONS, PAYMENT_MONEY
from tele_interface.static_text import from_eng_to_rus_day_week, NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER, \
    CHOOSE_TYPE_OF_PAYMENT
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
                     f'{user.first_name} {user.last_name} придёт '\
                     f'<b>в дополнительное время, не забудь взять {tarif}₽.</b>\n{date_info}'

    return user_text, admin_text
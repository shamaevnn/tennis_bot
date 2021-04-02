import datetime
from datetime import time, timedelta, datetime
from functools import wraps

from django.db.models import (ExpressionWrapper,
                              F, Q,
                              DateTimeField,
                              Count,
                              DurationField)
from django.db.models.functions import TruncDate

from base.models import (User,
                         GroupTrainingDay,
                         TrainingGroup, )
from base.utils import moscow_datetime

from tennis_bot.settings import DEBUG

import sys
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def handler_decor(check_status=False):
    """
    декоратор для всех handlers в телеграм боте
    :param check_status:
    :param bot:
    :return:
    """

    def decor(func):
        @wraps(func)
        def wrapper(bot, update):

            if DEBUG:
                logger.info(str(update) + '\n {}'.format(func.__name__))

            if update.callback_query:
                user_details = update.callback_query.from_user
            elif update.inline_query:
                user_details = update.inline_query.from_user
            else:
                user_details = update.message.from_user
            try:
                user = User.objects.get(
                    id=user_details.id,
                )

            except User.DoesNotExist:
                user = User.objects.create(
                    username='{}'.format(user_details.id),
                    id=user_details.id,
                    telegram_username=user_details.username[:64] if user_details.username else '',
                    first_name=user_details.first_name[:30] if user_details.first_name else '',
                    last_name=user_details.last_name[:60] if user_details.last_name else '',
                    password='1',
                )
                bot.send_message(user.id, 'Привет! Я бот самого продвинутого тренера в Туле (России).\
                 Для дальнейшей работы нужно указать свои контактные данные.')
                bot.send_message(user.id,
                                 'Введи фамилию и имя через пробел в формате "Фамилия Имя", например: Иванов Иван.')

            if user.is_blocked:
                user.is_blocked = False
                user.save()

            else:
                try:
                    if check_status:
                        if user.status != User.STATUS_WAITING and user.status != User.STATUS_FINISHED:
                            res = func(bot, update, user)
                        else:
                            bot.send_message(user.id, 'Тренер еще не одобрил.')
                    else:
                        res = func(bot, update, user)
                except Exception as e:
                    msg = f'{e}\n\nЧто-то пошло не так, напиши @ta2asho'
                    res = [bot.send_message(user.id, msg)]
                    tb = sys.exc_info()[2]
                    raise e.with_traceback(tb)

            return

        return wrapper

    return decor


def create_callback_data(purpose, action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([purpose, action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


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


def create_tr_days_for_future(instance):
    period = 8 if instance.group.status == TrainingGroup.STATUS_4IND else 24
    date = instance.date + timedelta(days=7)
    dates = [date]
    for _ in range(period):
        date += timedelta(days=7)
        dates.append(date)
    instances = [GroupTrainingDay(group=instance.group, date=dat, start_time=instance.start_time,
                                  duration=instance.duration) for dat in dates]
    GroupTrainingDay.objects.bulk_create(instances)
    

def get_available_dt_time4ind_train(duration: float, tr_day_date=moscow_datetime(datetime.now()).date()):
    # todo: какой-то пиздец, без пол литра не разберешься, хз шо с этим делать
    poss_date = moscow_datetime(datetime.now()).date()
    start_time = time(8, 0, 0)

    exist_tr_days = GroupTrainingDay.objects.tr_day_is_my_available(date=tr_day_date,
                                                                    start_time__gte=start_time).annotate(
        end_time=ExpressionWrapper(F('start_time') + F('duration'), output_field=DateTimeField()),
        date_tmp=TruncDate('date')).values('date_tmp', 'start_time', 'end_time').order_by('date', 'start_time')

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


def select_tr_days_for_skipping(user):
    tmp = GroupTrainingDay.objects.filter(Q(group__users__in=[user]) |
                                          Q(visitors__in=[user]) |
                                          Q(pay_visitors__in=[user]),
                                          date__gte=moscow_datetime(datetime.now()).date()).exclude(
        absent__in=[user]).order_by('id').distinct(
        'id').values('date', 'start_time')
    available_grouptraining_dates = [x['date'] for x in tmp
                                     if datetime.combine(x['date'],
                                                         x['start_time']) - moscow_datetime(datetime.now()) >
                                     user.time_before_cancel]
    return available_grouptraining_dates


def get_potential_days_for_group_training(user):
    potential_free_places = GroupTrainingDay.objects.tr_day_is_my_available().annotate(
        Count('absent', distinct=True),
        Count('group__users', distinct=True),
        Count('visitors', distinct=True),
        Count('pay_visitors', distinct=True),
        max_players=F('group__max_players'),
                    diff=ExpressionWrapper(F('start_time') + F('date') - moscow_datetime(datetime.now()),
                               output_field=DurationField()))\
            .annotate(all_users=F('pay_visitors__count')+F('visitors__count')+
                                F('group__users__count')-F('absent__count')).filter(
            Q(max_players__gt=F('all_users')) |
                (Q(max_players__lte=F('all_users')) & Q(group__available_for_additional_lessons=True) &
                 Q(max_players__lt=6) & Q(all_users__lt=6)),
                        diff__gte=timedelta(hours=1),
                        group__status=TrainingGroup.STATUS_GROUP,
                ).exclude(
                    Q(visitors__in=[user]) | Q(group__users__in=[user])).order_by('start_time')

    return potential_free_places


def balls_lessons_payment(year, month, user):
    tr_days_this_month = GroupTrainingDay.objects.filter(date__year=year, date__month=month, is_available=True)
    num_of_group_lessons = 0
    if user.status == User.STATUS_TRAINING:
        tr_days_num_this_month = tr_days_this_month.filter(group__users__in=[user],
                                                           group__status=TrainingGroup.STATUS_GROUP).distinct()
        num_of_group_lessons = tr_days_num_this_month.count()
        balls_this_month = tr_days_num_this_month.count()

        group = TrainingGroup.objects.filter(users__in=[user], max_players__gte=3).first()
        tarif = group.tarif_for_one_lesson if group else 0

    elif user.status == User.STATUS_ARBITRARY:
        tr_days_num_this_month = tr_days_this_month.filter(visitors__in=[user]).distinct()
        balls_this_month = 0
        tarif = User.tarif_for_status[user.status]

    should_pay_this_month = tr_days_num_this_month.count() * tarif
    should_pay_balls = 100 * round(balls_this_month / 4)

    return should_pay_this_month, should_pay_balls, num_of_group_lessons

import logging

from datetime import timedelta

from base.models import (User,
                         GroupTrainingDay,
                         TrainingGroup, )
from tele_interface.static_text import COACH_HAVE_NOT_CONFIRMED_YET

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


def check_status_decor(func):
    def wrapper(update, context):
        res = None
        user, _ = User.get_user_and_created(update, context)
        if user.status != User.STATUS_WAITING and user.status != User.STATUS_FINISHED:
            res = func(update, context)
        else:
            context.bot.send_message(user.id,
                                     COACH_HAVE_NOT_CONFIRMED_YET)
        return res

    return wrapper


def create_callback_data(purpose, action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([purpose, action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_tr_days_for_future(instance):
    period = 8 if instance.group.status == TrainingGroup.STATUS_4IND else 24
    date = instance.date + timedelta(days=7)
    dates = [date]
    for _ in range(period):
        date += timedelta(days=7)
        dates.append(date)
    instances = [GroupTrainingDay(
        group=instance.group,
        date=dat,
        start_time=instance.start_time,
        duration=instance.duration,
        is_individual=instance.is_individual
    ) for dat in dates]
    GroupTrainingDay.objects.bulk_create(instances)



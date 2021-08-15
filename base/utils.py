from datetime import timedelta

from base.models import TrainingGroup, GroupTrainingDay


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

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


def extract_user_data_from_update(update):
    """ python-telegram-bot's Update instance --> User info """
    if update.message is not None:
        user = update.message.from_user.to_dict()
    elif update.inline_query is not None:
        user = update.inline_query.from_user.to_dict()
    elif update.chosen_inline_result is not None:
        user = update.chosen_inline_result.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.from_user is not None:
        user = update.callback_query.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.message is not None:
        user = update.callback_query.message.chat.to_dict()
    else:
        raise Exception(f"Can't extract user data from update: {update}")

    return dict(
        id=user["id"],
        is_blocked=False,
        **{
            k: user[k]
            for k in ["username", "first_name", "last_name"]
            if k in user and user[k] is not None
        },
    )
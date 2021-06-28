from django.db.models import QuerySet

from base.models import GroupTrainingDay, User, TrainingGroup


def balls_lessons_payment(year, month, user):
    tr_days_this_month: QuerySet[GroupTrainingDay] = GroupTrainingDay.objects.filter(
        date__year=year,
        date__month=month,
        is_available=True
    )
    num_of_group_lessons = 0
    if user.status == User.STATUS_TRAINING:
        tr_days_num_this_month: int = tr_days_this_month.filter(
            group__users__in=[user], group__status=TrainingGroup.STATUS_GROUP
        ).distinct().count()
        num_of_group_lessons: int = tr_days_num_this_month
        balls_this_month: int = tr_days_num_this_month

        group: TrainingGroup = TrainingGroup.objects.filter(users__in=[user], max_players__gte=3).first()
        tarif: int = group.tarif_for_one_lesson if group else 0

    elif user.status == User.STATUS_ARBITRARY:
        tr_days_num_this_month: int = tr_days_this_month.filter(visitors__in=[user]).distinct().count()
        balls_this_month: int = 0
        tarif: int = User.tarif_for_status[user.status]

    else:
        tarif: int = 0
        tr_days_num_this_month: int = 0
        balls_this_month: int = 0

    should_pay_this_month = tr_days_num_this_month * tarif
    should_pay_balls = 100 * round(balls_this_month / 4)

    return should_pay_this_month, should_pay_balls, num_of_group_lessons
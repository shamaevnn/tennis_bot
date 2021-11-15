from typing import Union

from django.db.models import Sum, Count, Q, ExpressionWrapper, F, IntegerField, QuerySet

from base.models import Payment, TrainingGroup, Player


def get_total_paid_amount_for_month(year: int, month: int) -> int:
    amount_for_this_month = Payment.objects.filter(
        year=year, month=month
    ).aggregate(sigma=Sum('fact_amount'))

    return amount_for_this_month["sigma"] if amount_for_this_month["sigma"] else 0


def get_total_should_pay_amount(year: Union[str, int], month: Union[str, int]) -> int:
    should_pay_this_month = TrainingGroup.objects.annotate(
        count_tr_days=Count(
            'grouptrainingday',
            filter=Q(
                grouptrainingday__is_available=True,
                grouptrainingday__date__month=month,
                grouptrainingday__date__year=int(year) + 2020
            ),
            distinct=True
        ),
        count_players=Count(
            'players',
            distinct=True
        )
    ).filter(
        max_players__gt=1
    ).annotate(
        should_pay=ExpressionWrapper(
            F('count_players') * F('tarif_for_one_lesson') * F('count_tr_days'),
            output_field=IntegerField(),
        )
    ).aggregate(
        sigma=Sum('should_pay')
    )
    return should_pay_this_month["sigma"] if should_pay_this_month["sigma"] else 0


def get_not_paid_payments(year: Union[str, int], month: Union[str, int]) -> QuerySet[Payment]:
    payments = Payment.objects.filter(
        player__status=Player.STATUS_TRAINING,
        fact_amount=0,
        month=month,
        year=year
    ).annotate(
        group_name=F('player__traininggroup__name'),
        group_status=F('player__traininggroup__status'),
        group_order=F('player__traininggroup__order')
    ).filter(
        group_status=TrainingGroup.STATUS_GROUP
    )
    return payments

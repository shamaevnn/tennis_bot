from datetime import timedelta, datetime

from django.db.models import Count, F, ExpressionWrapper, DurationField, Q

from base.common_for_bots.utils import moscow_datetime
from base.models import GroupTrainingDay, TrainingGroup, Player


def get_potential_days_for_group_training(player: Player, **filters):
    potential_free_places = (
        GroupTrainingDay.objects.tr_day_is_my_available(
            group__status=TrainingGroup.STATUS_GROUP, is_individual=False
        )
        .annotate(
            Count("absent", distinct=True),
            Count("group__players", distinct=True),
            Count("visitors", distinct=True),
            Count("pay_visitors", distinct=True),
            Count("pay_bonus_visitors", distinct=True),
            max_players=F("group__max_players"),
            diff=ExpressionWrapper(
                F("start_time") + F("date") - moscow_datetime(datetime.now()),
                output_field=DurationField(),
            ),
        )
        .annotate(
            all_players=F("pay_visitors__count")
            + F("visitors__count")
            + F("pay_bonus_visitors__count")
            + F("group__players__count")
            - F("absent__count")
        )
        .filter(
            Q(max_players__gt=F("all_players"))
            | (
                Q(max_players__lte=F("all_players"))
                & Q(group__available_for_additional_lessons=True)
                & Q(max_players__lt=6)
                & Q(all_players__lt=6)
            ),
            diff__gte=timedelta(microseconds=5),
            max_players__gt=1,
            **filters
        )
        .exclude(
            Q(visitors__in=[player])
            | Q(group__players__in=[player])
            | Q(pay_visitors__in=[player])
            | Q(pay_bonus_visitors__in=[player])
        )
        .order_by("start_time")
    )

    return potential_free_places

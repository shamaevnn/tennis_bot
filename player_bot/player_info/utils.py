from django.db.models import QuerySet

from base.models import GroupTrainingDay, Player, TrainingGroup


def balls_lessons_payment(year: int, month: int, player: Player):
    tr_days_this_month: QuerySet[GroupTrainingDay] = GroupTrainingDay.objects.filter(
        date__year=year, date__month=month, is_available=True
    )

    if player.status == Player.STATUS_TRAINING:
        tr_days_num_this_month: int = (
            tr_days_this_month.filter(
                group__players__in=[player], group__status=TrainingGroup.STATUS_GROUP
            )
            .distinct()
            .count()
        )
        balls_this_month: int = tr_days_num_this_month

        group: TrainingGroup = TrainingGroup.objects.filter(
            players__in=[player], status=TrainingGroup.STATUS_GROUP
        ).first()
        tarif: int = group.tarif_for_one_lesson if group else 0
    elif player.status == Player.STATUS_ARBITRARY:
        tr_days_num_this_month: int = (
            tr_days_this_month.filter(visitors__in=[player]).distinct().count()
        )
        balls_this_month: int = 0
        tarif: int = Player.get_tarif_by_status(player.status)
    else:
        tarif: int = 0
        tr_days_num_this_month: int = 0
        balls_this_month: int = 0

    should_pay_this_month = tr_days_num_this_month * tarif
    should_pay_balls = 100 * round(balls_this_month / 4)

    return should_pay_this_month, should_pay_balls


def group_players_info(players: QuerySet[Player]):
    return "\n".join(
        (
            f"👤{x['last_name']} {x['first_name']}"
            for x in players.values("first_name", "last_name").order_by("last_name")
        )
    )

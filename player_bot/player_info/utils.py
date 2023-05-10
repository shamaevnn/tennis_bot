from django.db.models import QuerySet

from base.models import GroupTrainingDay, Player, TrainingGroup
from tennis_bot.settings import BALLS_PRICE_FOR_1_TRAIN_PER_WEEK


def balls_lessons_payment(year: int, month: int, player: Player):
    tr_days_this_month: QuerySet[GroupTrainingDay] = GroupTrainingDay.objects.filter(
        date__year=year, date__month=month, available_status= GroupTrainingDay.AVAILABLE, 
    )

    if player.status == Player.STATUS_TRAINING:
        tr_days_num_this_month: int = (
            tr_days_this_month.filter(
                group__players__in = [player], 
                group__status = TrainingGroup.STATUS_GROUP
            )
            .distinct()
            .count()
        )
        should_pay_balls = BALLS_PRICE_FOR_1_TRAIN_PER_WEEK * round(
            tr_days_num_this_month / 4
        )

        group: TrainingGroup = TrainingGroup.objects.filter(
            players__in=[player], 
            status=TrainingGroup.STATUS_GROUP,
        ).first()
        tarif: int = group.tarif_for_one_lesson if group else 0
        
    elif player.status == Player.STATUS_ARBITRARY:
        tr_days_num_this_month: int = (
            tr_days_this_month.filter(visitors__in=[player]).distinct().count()
        )
        should_pay_balls: int = 0
        tarif: int = Player.get_tarif_by_status(player.status)
    else:
        tarif: int = 0
        tr_days_num_this_month: int = 0
        should_pay_balls: int = 0

    should_pay_this_month = tr_days_num_this_month * tarif
    return should_pay_this_month, should_pay_balls


def group_players_info(players: QuerySet[Player]):
    return "\n".join(
        (
            f"👤{x['last_name']} {x['first_name']}"
            for x in players.values("first_name", "last_name").order_by("last_name")
        )
    )

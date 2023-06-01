import datetime

from django.db.models import QuerySet

from base.models import GroupTrainingDay, Player, TrainingGroup, PlayerCancelLesson
from tennis_bot.settings import BALLS_PRICE_FOR_1_TRAIN_PER_WEEK


def calculation_lessons_payment(year: int, month: int, player: Player):
    tr_days_this_month: QuerySet[GroupTrainingDay] = GroupTrainingDay.objects.filter(
        date__year=year,
        date__month=month,
        available_status=GroupTrainingDay.AVAILABLE,
    )

    if player.status == Player.STATUS_TRAINING:
        tr_days_num_this_month: int = (
            tr_days_this_month.filter(
                group__players__in=[player], group__status=TrainingGroup.STATUS_GROUP
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

    pay_cancels = 0
    cancels_count = 0

    prev_month = get_prev_month(month)
    first_date_of_prev_month = datetime.date.today().replace(month=prev_month, day=1)
    cancel = PlayerCancelLesson.get_cancel_from_player(player, first_date_of_prev_month)
    if cancel is not None:
        # если есть отмены за прошлый месяц
        cancels_count = cancel.n_cancelled_lessons
        pay_cancels = cancel.n_cancelled_lessons * tarif

    should_pay_this_month_without_cancels = tr_days_num_this_month * tarif
    should_pay_this_month = should_pay_this_month_without_cancels - pay_cancels
    if should_pay_this_month < 0:
        should_pay_this_month_without_cancels = 0
        should_pay_this_month = 0
        should_pay_balls = 0
        pay_cancels = 0

    return (
        should_pay_this_month,
        should_pay_this_month_without_cancels,
        should_pay_balls,
        pay_cancels,
        cancels_count,
    )


def group_players_info(players: QuerySet[Player]):
    return "\n".join(
        (
            f"👤{x['last_name']} {x['first_name']}"
            for x in players.values("first_name", "last_name").order_by("last_name")
        )
    )


def get_prev_month(month):
    return 12 if month == 1 else month - 1
    # prev_month = month
    # if prev_month > 1:
    #     prev_month = prev_month - 1
    #
    # elif prev_month == 1:
    #     prev_month = 12
    #
    # return prev_month


def get_next_month(month: int) -> int:
    return 1 if month == 12 else month + 1

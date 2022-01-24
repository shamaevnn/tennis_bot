from datetime import datetime
from typing import Tuple, Iterator

from django.db.models import Q

from player_bot.skip_lesson.static_text import (
    PLAYER_CANCELLED_IND_TRAIN,
    PLAYER_SKIPPED_TRAIN_FOR_BONUS,
    PLAYER_SKIPPED_TRAIN_FOR_MONEY,
    PLAYER_SKIPPED_TRAIN_FOR_PAY_BONUS,
    PLAYER_SKIPPED_TRAIN_IN_HIS_GROUP,
    CANT_CANCEL_LESSON_TOO_LATE,
    OKAY_TRAIN_CANCELLED,
    PLAYER_CANCELLED_RENT_COURT,
)
from base.common_for_bots.static_text import ATTENTION
from base.models import GroupTrainingDay, Player
from base.common_for_bots.utils import (
    get_actual_players_without_absent,
    moscow_datetime,
    create_calendar,
)
from player_bot.skip_lesson.keyboards import (
    construct_menu_skipping_much_lesson,
    construct_detail_menu_for_skipping,
)


def select_tr_days_for_skipping(
    player: Player, **filters
) -> Iterator[GroupTrainingDay]:
    now = moscow_datetime(datetime.now())
    tr_days_of_player = (
        GroupTrainingDay.objects.filter(
            Q(group__players__in=[player])
            | Q(visitors__in=[player])
            | Q(pay_visitors__in=[player])
            | Q(pay_bonus_visitors__in=[player]),
            date__gte=now.date(),
            **filters,
        )
        .exclude(absent__in=[player])
        .select_related("group")
        .order_by("id")
        .iterator()
    )

    for tr_day in tr_days_of_player:
        if (
            tr_day.start_dttm > now
            and tr_day.start_dttm - now > player.time_before_cancel
        ):
            yield tr_day


def make_group_name_group_players_info_for_skipping(
    tr_day: GroupTrainingDay,
) -> Tuple[str, str]:
    all_players = get_actual_players_without_absent(tr_day).values(
        "first_name", "last_name"
    )

    all_players = "\n".join(
        (f"{x['first_name']} {x['last_name']}" for x in all_players)
    )

    tr_day_status = tr_day.status

    if tr_day_status == GroupTrainingDay.INDIVIDUAL_TRAIN:
        group_name = "🧞‍♂индивидуальная тренировка🧞‍♂️\n"
        group_players = ""
    elif tr_day_status == GroupTrainingDay.RENT_COURT_STATUS:
        group_name = "💸 аренда корта ️💸\n"
        group_players = ""
    else:
        group_name = f"{tr_day.group.name}\n"
        group_players = f"Присутствующие:\n{all_players}\n"

    return group_name, group_players


def calendar_skipping(player: Player, purpose, date_my):
    training_days = list(set(select_tr_days_for_skipping(player, date=date_my)))
    if len(training_days):
        # несколько тренировок в один день
        if len(training_days) > 1:
            markup = construct_menu_skipping_much_lesson(training_days)
            text = "Выбери время"
        else:
            training_day = training_days[0]
            group_name, group_players = make_group_name_group_players_info_for_skipping(
                training_day
            )

            markup, text = construct_detail_menu_for_skipping(
                training_day, purpose, group_name, group_players
            )
    else:
        text = (
            "Нет тренировки в этот день, выбери другой.\n"
            "✅ -- дни, доступные для отмены."
        )

        markup = create_calendar(
            purpose,
            date_my.year,
            date_my.month,
            dates_to_highlight=[
                tr_day.date for tr_day in select_tr_days_for_skipping(player)
            ],
        )
    return text, markup


def handle_skipping_train(
    training_day: GroupTrainingDay, player: Player, date_info: str
):
    text = OKAY_TRAIN_CANCELLED.format(date_info)

    tr_day_status = training_day.status

    if tr_day_status == GroupTrainingDay.RENT_COURT_STATUS:
        training_day.delete()
        admin_text = PLAYER_CANCELLED_RENT_COURT.format(
            ATTENTION, player.first_name, player.last_name, date_info
        )
        return text, admin_text
    elif tr_day_status == GroupTrainingDay.INDIVIDUAL_TRAIN:
        training_day.delete()
        admin_text = PLAYER_CANCELLED_IND_TRAIN.format(
            ATTENTION, player.first_name, player.last_name, date_info
        )
        return text, admin_text

    if (
        datetime.combine(training_day.date, training_day.start_time)
        - moscow_datetime(datetime.now())
        < player.time_before_cancel
    ):
        text = CANT_CANCEL_LESSON_TOO_LATE.format(
            round(player.time_before_cancel.seconds / 3600)
        )
        admin_text = ""
        return text, admin_text

    if player in training_day.visitors.all():
        player.bonus_lesson += 1
        training_day.visitors.remove(player)
        admin_text = PLAYER_SKIPPED_TRAIN_FOR_BONUS.format(
            player.first_name, player.last_name, date_info
        )
    elif player in training_day.pay_visitors.all():
        # в этом случае не должно поменяться кол-во отыгрышей
        training_day.pay_visitors.remove(player)
        admin_text = PLAYER_SKIPPED_TRAIN_FOR_MONEY.format(
            player.first_name, player.last_name, date_info
        )
    elif player in training_day.pay_bonus_visitors.all():
        player.bonus_lesson += 1
        training_day.pay_bonus_visitors.remove(player)
        admin_text = PLAYER_SKIPPED_TRAIN_FOR_PAY_BONUS.format(
            player.first_name, player.last_name, date_info
        )
    else:
        player.bonus_lesson += 1
        training_day.absent.add(player)
        admin_text = PLAYER_SKIPPED_TRAIN_IN_HIS_GROUP.format(
            player.first_name, player.last_name, date_info
        )
    player.save()
    return text, admin_text

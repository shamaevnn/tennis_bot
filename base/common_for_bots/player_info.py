from calendar import monthrange
from datetime import date, datetime, timedelta

from base.common_for_bots.player_payment import calculation_lessons_payment
from base.common_for_bots.static_text import from_digit_to_month, PAYMENT_REQUISITES
from base.common_for_bots.utils import moscow_datetime, get_prev_month
from base.models import Player, Payment, TrainingGroup, PlayerCancelLesson
from player_bot.player_info.static_text import (
    NO_PAYMENT_BUTTON,
    SUCCESS_PAYMENT,
    INTRO_INFO_TEMPLATE,
    GROUP_INFO_TEMPLATE,
    BONUS_LESSON_COUNT_INFO,
    N_CANCELLED_LESSON_COUNT_INFO,
    SHOULD_PAY_INFO_THIS_MONTH,
    SHOULD_PAY_INFO_NEXT_MONTH,
    SHOULD_PAY_INFO,
)


def _get_payment_status(player: Player, today_date: date) -> str:
    player_payment = Payment.objects.filter(
        player=player,
        player__status=Player.STATUS_TRAINING,
        fact_amount=0,
        year=today_date.year - 2020,
        month=today_date.month,
    )

    if player.status == Player.STATUS_TRAINING:
        if player_payment.exists():
            payment_status = f"{NO_PAYMENT_BUTTON}\n"
        else:
            payment_status = f"{SUCCESS_PAYMENT}\n"
    else:
        payment_status = ""
    return payment_status


def _get_intro(player: Player) -> str:
    from_player_to_intro = {
        Player.STATUS_WAITING: "в листе ожидания.",
        Player.STATUS_TRAINING: "тренируешься в группе.",
        Player.STATUS_FINISHED: "закончил тренировки.",
        Player.STATUS_ARBITRARY: "тренируешься по свободному графику.",
    }

    intro = INTRO_INFO_TEMPLATE.format(from_player_to_intro[player.status])
    return intro


def _get_group_info(player: Player) -> str:
    group = (
        TrainingGroup.objects.filter(players__in=[player])
        .exclude(max_players=1)
        .first()
    )

    teammates = group.players.all() if group else Player.objects.none()

    players_info = "\n".join(
        (
            f"👤{x['last_name']} {x['first_name']}"
            for x in teammates.values("first_name", "last_name").order_by("last_name")
        )
    )
    group_info = (
        GROUP_INFO_TEMPLATE.format(group.name, players_info) if teammates else ""
    )
    return group_info


def _get_number_of_bonus_lessons(player: Player) -> str:
    return BONUS_LESSON_COUNT_INFO.format(player.bonus_lesson)


def _get_n_cancelled_lessons(player: Player) -> str:
    cancel = PlayerCancelLesson.get_cancel_from_player(player, date.today())
    _n_cancelled_lessons = 0 if cancel is None else cancel.n_cancelled_lessons
    cancelled_lessons = N_CANCELLED_LESSON_COUNT_INFO.format(_n_cancelled_lessons)
    return cancelled_lessons


def _get_payment_info(player: Player, today_date: date) -> str:
    number_of_days_in_month = monthrange(today_date.year, today_date.month)[1]
    last_day = date(today_date.year, today_date.month, number_of_days_in_month)
    next_month = last_day + timedelta(days=1)

    (
        should_pay_this_month,
        should_pay_this_month_without_cancells,
        balls_this_month,
        pay_cancels,
        cancel_count,
    ) = calculation_lessons_payment(today_date.year, today_date.month, player)
    (
        should_pay_money_next,
        should_pay_next_month_without_cancells,
        balls_next_month,
        pay_next_cancels,
        cancel_next_count,
    ) = calculation_lessons_payment(next_month.year, next_month.month, player)

    prev_month = get_prev_month(today_date.month)
    this_month_pay_info = SHOULD_PAY_INFO_THIS_MONTH.format(
        from_digit_to_month[today_date.month],
        should_pay_this_month,
        should_pay_this_month_without_cancells,
        from_digit_to_month[today_date.month],
        pay_cancels,
        cancel_count,
        from_digit_to_month[prev_month],
        balls_this_month,
    )

    next_month_pay_info = SHOULD_PAY_INFO_NEXT_MONTH.format(
        from_digit_to_month[next_month.month],
        should_pay_money_next,
        should_pay_next_month_without_cancells,
        from_digit_to_month[next_month.month],
        pay_next_cancels,
        cancel_next_count,
        from_digit_to_month[today_date.month],
        balls_next_month,
    )

    should_pay_info = SHOULD_PAY_INFO.format(
        this_month_pay_info,
        next_month_pay_info,
        PAYMENT_REQUISITES,
    )
    return should_pay_info


def get_player_info(player: Player) -> str:
    today_date = moscow_datetime(datetime.now()).date()
    payment_status = _get_payment_status(player, today_date)
    intro = _get_intro(player)
    group_info = _get_group_info(player)
    bonus_lessons = _get_number_of_bonus_lessons(player)
    cancelled_lesson = _get_n_cancelled_lessons(player)
    should_pay_info = _get_payment_info(player, today_date)

    text = (
        intro
        + group_info
        + bonus_lessons
        + cancelled_lesson
        + payment_status
        + should_pay_info
    )
    return text

from calendar import monthrange
from datetime import date, datetime, timedelta

from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from base.models import Payment, TrainingGroup, Player, PlayerCancelLesson
from player_bot.menu_and_commands.keyboards import construct_main_menu
from base.common_for_bots.utils import moscow_datetime

from player_bot.player_info.static_text import (
    BONUS_LESSON_COUNT_INFO,
    INTRO_INFO_TEMPLATE,
    GROUP_INFO_TEMPLATE,
    N_CANCELLED_LESSON_COUNT_INFO,
    NO_PAYMENT_BUTTON,
    MY_DATA_BUTTON,
    SHOULD_PAY_INFO,
    SHOULD_PAY_INFO_THIS_MONTH,
    SHOULD_PAY_INFO_NEXT_MONTH,
    SUCCESS_PAYMENT,
)

from base.common_for_bots.static_text import PAYMENT_REQUISITES, from_digit_to_month
from player_bot.registration.utils import check_status_decor
from player_bot.player_info.utils import (
    balls_lessons_payment,
    group_players_info,
    get_prev_month,
)


@check_status_decor
def player_main_info(update: Update, context: CallbackContext):
    """посмотреть, основную инфу:
    статус
    группа, если есть
    отыгрыши
    сколько должен заплатить
    """

    from_player_to_intro = {
        Player.STATUS_WAITING: "в листе ожидания.",
        Player.STATUS_TRAINING: "тренируешься в группе.",
        Player.STATUS_FINISHED: "закончил тренировки.",
        Player.STATUS_ARBITRARY: "тренируешься по свободному графику.",
    }

    today_date = date.today()
    player, _ = Player.get_player_and_created(update, context)
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

    intro = INTRO_INFO_TEMPLATE.format(from_player_to_intro[player.status])

    group = (
        TrainingGroup.objects.filter(players__in=[player])
        .exclude(max_players=1)
        .first()
    )

    teammates = group.players.all() if group else Player.objects.none()

    group_info = (
        GROUP_INFO_TEMPLATE.format(group.name, group_players_info(teammates))
        if teammates
        else ""
    )

    number_of_add_games = BONUS_LESSON_COUNT_INFO.format(player.bonus_lesson)

    cancel = PlayerCancelLesson.get_cancel_from_player(player, date.today())
    _n_cancelled_lessons = 0 if cancel is None else cancel.n_cancelled_lessons
    cancelled_games = N_CANCELLED_LESSON_COUNT_INFO.format(_n_cancelled_lessons)

    today = moscow_datetime(datetime.now()).date()
    number_of_days_in_month = monthrange(today.year, today.month)[1]
    last_day = date(today.year, today.month, number_of_days_in_month)
    next_month = last_day + timedelta(days=1)

    (
        should_pay_this_month,
        should_pay_this_month_without_cancells,
        balls_this_month,
        pay_cancels,
        cancel_count,
    ) = balls_lessons_payment(today.year, today.month, player)
    (
        should_pay_money_next,
        should_pay_next_month_without_cancells,
        balls_next_month,
        pay_next_cancels,
        cancel_next_count,
    ) = balls_lessons_payment(next_month.year, next_month.month, player)

    prev_month = get_prev_month(today.month)

    this_month_pay_info = SHOULD_PAY_INFO_THIS_MONTH.format(
        from_digit_to_month[today.month],
        should_pay_this_month,
        should_pay_this_month_without_cancells,
        from_digit_to_month[today.month],
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
        from_digit_to_month[today.month],
        balls_next_month,
    )

    should_pay_info = SHOULD_PAY_INFO.format(
        this_month_pay_info,
        next_month_pay_info,
        PAYMENT_REQUISITES,
    )

    text = (
        intro
        + group_info
        + number_of_add_games
        + cancelled_games
        + payment_status
        + should_pay_info
    )

    update.message.reply_text(
        text=text, parse_mode="HTML", reply_markup=construct_main_menu(player)
    )
    return ConversationHandler.END

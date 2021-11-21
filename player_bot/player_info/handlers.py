from calendar import monthrange
from datetime import date, datetime, timedelta

from telegram.ext import ConversationHandler

from base.models import Payment, TrainingGroup, Player
from player_bot.menu_and_commands.keyboards import construct_main_menu
from base.common_for_bots.utils import moscow_datetime
from player_bot.player_info.static_text import NO_PAYMENT_BUTTON, SUCCESS_PAYMENT
from base.common_for_bots.static_text import from_digit_to_month
from player_bot.registration.utils import check_status_decor
from player_bot.player_info.utils import balls_lessons_payment, group_players_info


@check_status_decor
def player_main_info(update, context):
    """посмотреть, основную инфу:
        статус
        группа, если есть
        отыгрыши
        сколько должен заплатить
    """

    from_player_to_intro = {
        Player.STATUS_WAITING: 'в листе ожидания.',
        Player.STATUS_TRAINING: 'тренируешься в группе.',
        Player.STATUS_FINISHED: 'закончил тренировки.',
        Player.STATUS_ARBITRARY: 'тренируешься по свободному графику.'
    }

    today_date = date.today()
    player, _ = Player.get_player_and_created(update, context)
    player_payment = Payment.objects.filter(player=player, player__status=Player.STATUS_TRAINING, fact_amount=0,
                                          year=today_date.year - 2020, month=today_date.month)

    if player.status == Player.STATUS_TRAINING:
        if player_payment.exists():
            payment_status = f'{NO_PAYMENT_BUTTON}\n'
        else:
            payment_status = f'{SUCCESS_PAYMENT}\n'
    else:
        payment_status = ''

    intro = f'В данный момент ты {from_player_to_intro[player.status]}\n\n'

    group = TrainingGroup.objects.filter(players__in=[player]).exclude(max_players=1).first()

    teammates = group.players.all() if group else Player.objects.none()

    group_info = "Твоя группа -- {}:\n{}\n\n".format(group.name, group_players_info(teammates)) if teammates else ''

    number_of_add_games = 'Количество отыгрышей: <b>{}</b>\n\n'.format(player.bonus_lesson)

    today = moscow_datetime(datetime.now()).date()
    number_of_days_in_month = monthrange(today.year, today.month)[1]
    last_day = date(today.year, today.month, number_of_days_in_month)
    next_month = last_day + timedelta(days=1)

    should_pay_this_month, balls_this_month = balls_lessons_payment(today.year, today.month, player)
    should_pay_money_next, balls_next_month = balls_lessons_payment(next_month.year, next_month.month, player)

    should_pay_info = 'В этом месяце ({}) <b>нужно заплатить {} ₽ + {} ₽ за мячи.</b>\n' \
                      'В следующем месяце ({}) <b>нужно заплатить {} ₽ + {} ₽ за мячи</b>.'.format(
        from_digit_to_month[today.month], should_pay_this_month, balls_this_month,
        from_digit_to_month[next_month.month], should_pay_money_next, balls_next_month
    )

    text = intro + group_info + number_of_add_games + payment_status + should_pay_info

    update.message.reply_text(
        text=text,
        parse_mode='HTML',
        reply_markup=construct_main_menu(player)
    )
    return ConversationHandler.END

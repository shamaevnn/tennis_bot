from calendar import monthrange
from datetime import date, datetime, timedelta

from telegram.ext import ConversationHandler

from base.models import User, Payment, TrainingGroup
from player_bot.menu_and_commands.keyboard_utils import construct_main_menu
from base.common_for_bots.utils import moscow_datetime
from player_bot.user_info.static_text import NO_PAYMENT_BUTTON, SUCCESS_PAYMENT
from base.common_for_bots.static_text import from_digit_to_month
from player_bot.registration.utils import check_status_decor
from player_bot.user_info.utils import balls_lessons_payment, group_users_info


@check_status_decor
def user_main_info(update, context):
    """посмотреть, основную инфу:
        статус
        группа, если есть
        отыгрыши
        сколько должен заплатить
    """

    from_user_to_intro = {
        User.STATUS_WAITING: 'в листе ожидания.',
        User.STATUS_TRAINING: 'тренируешься в группе.',
        User.STATUS_FINISHED: 'закончил тренировки.',
        User.STATUS_ARBITRARY: 'тренируешься по свободному графику.'
    }

    today_date = date.today()
    user, _ = User.get_user_and_created(update, context)
    user_payment = Payment.objects.filter(player=user, player__status=User.STATUS_TRAINING, fact_amount=0,
                                          year=today_date.year - 2020, month=today_date.month)

    if user.status == User.STATUS_TRAINING:
        if user_payment.exists():
            payment_status = f'{NO_PAYMENT_BUTTON}\n'
        else:
            payment_status = f'{SUCCESS_PAYMENT}\n'
    else:
        payment_status = ''

    intro = f'В данный момент ты {from_user_to_intro[user.status]}\n\n'

    group = TrainingGroup.objects.filter(users__in=[user]).exclude(max_players=1).first()

    teammates = group.users.all() if group else User.objects.none()

    group_info = "Твоя группа -- {}:\n{}\n\n".format(group.name, group_users_info(teammates)) if teammates else ''

    number_of_add_games = 'Количество отыгрышей: <b>{}</b>\n\n'.format(user.bonus_lesson)

    today = moscow_datetime(datetime.now()).date()
    number_of_days_in_month = monthrange(today.year, today.month)[1]
    last_day = date(today.year, today.month, number_of_days_in_month)
    next_month = last_day + timedelta(days=1)

    should_pay_this_month, balls_this_month = balls_lessons_payment(today.year, today.month, user)
    should_pay_money_next, balls_next_month = balls_lessons_payment(next_month.year, next_month.month, user)

    should_pay_info = 'В этом месяце ({}) <b>нужно заплатить {} ₽ + {} ₽ за мячи.</b>\n' \
                      'В следующем месяце ({}) <b>нужно заплатить {} ₽ + {} ₽ за мячи</b>.'.format(
        from_digit_to_month[today.month], should_pay_this_month, balls_this_month,
        from_digit_to_month[next_month.month], should_pay_money_next, balls_next_month
    )

    text = intro + group_info + number_of_add_games + payment_status + should_pay_info

    update.message.reply_text(
        text=text,
        parse_mode='HTML',
        reply_markup=construct_main_menu(user)
    )
    return ConversationHandler.END

import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum, Count, Q, ExpressionWrapper, F, IntegerField
from telegram.ext import ConversationHandler

import base.common_for_bots.tasks
from admin_bot.payment.keyboard_utils import construct_menu_groups, construct_menu_months
from admin_bot.payment import keyboard_utils
from admin_bot.payment import manage_data
from admin_bot.payment import static_text
from admin_bot.payment.utils import check_if_players_not_in_payments, have_not_paid_users_info
from base.models import Payment, TrainingGroup, User, GroupTrainingDay
from base.common_for_bots.utils import moscow_datetime, bot_edit_message, info_about_users

from base.common_for_bots.static_text import from_digit_to_month, UP_TO_YOU
from tennis_bot.settings import TARIF_SECTION, TARIF_FEW


START_CHANGE_PAYMENT, CONFIRM_OR_CANCEL = range(2)


def start_payment(update, context):
    text = static_text.CHOOSE_YEAR
    now_date = moscow_datetime(datetime.datetime.now()).date()
    markup = keyboard_utils.choose_year_to_group_payment_keyboard(
        year=now_date.year,
        month=now_date.month
    )

    if update.callback_query:
        bot_edit_message(context.bot, text, update, markup)
    else:
        update.message.reply_text(
            text=text,
            reply_markup=markup
        )


def year_payment(update, context):
    year = update.callback_query.data[len(manage_data.PAYMENT_YEAR):]
    markup = construct_menu_months(Payment.MONTHS, f'{manage_data.PAYMENT_YEAR_MONTH}{year}|')
    bot_edit_message(context.bot, static_text.CHOOSE_MONTH, update, markup)


def month_payment(update, context):
    year, month = update.callback_query.data[len(manage_data.PAYMENT_YEAR_MONTH):].split('|')

    amount_for_this_month = Payment.objects.filter(year=year, month=month).aggregate(sigma=Sum('fact_amount'))

    should_pay_this_month = TrainingGroup.objects.annotate(
        count_tr_days=Count('grouptrainingday',
                            filter=Q(
                                grouptrainingday__is_available=True,
                                grouptrainingday__date__month=month,
                                grouptrainingday__date__year=int(year) + 2020),
                            distinct=True
                            ),
        count_users=Count('users', distinct=True)
    ).filter(
        max_players__gt=1
    ).annotate(
        should_pay=ExpressionWrapper(
            F('count_users') * F('tarif_for_one_lesson') * F('count_tr_days'),
            output_field=IntegerField()
        )
    ).aggregate(sigma=Sum('should_pay'))

    text = f'{int(year) + 2020}--{from_digit_to_month[int(month)]}\n' \
           f'<b>{static_text.TOTAL_PAID}: {amount_for_this_month["sigma"] if amount_for_this_month["sigma"] else 0}</b>\n' \
           f'<b>{static_text.MUST_PAY}: {should_pay_this_month["sigma"]}</b>\n' \
           f'{static_text.CHOOSE_GROUP}'

    banda_groups = TrainingGroup.objects.filter(name__iregex=r'БАНДА').order_by('order')
    markup = construct_menu_groups(banda_groups, f'{manage_data.PAYMENT_YEAR_MONTH_GROUP}{year}|{month}|')
    bot_edit_message(context.bot, text, update, markup)

    return ConversationHandler.END


def group_payment(update, context):
    year, month, group_id = update.callback_query.data[len(manage_data.PAYMENT_YEAR_MONTH_GROUP):].split('|')

    if int(group_id) == 0:
        # нажал на "не заплатили"
        title = f'{static_text.HAVE_NOT_PAID}\n'

        payments = Payment.objects.filter(
            player__status=User.STATUS_TRAINING,
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

        help_info = static_text.FIRST_LAST_NAME_NUMBER_OF_VISITS_GROUP if payments.exists() else static_text.NO_SUCH
        for payment in payments:
            payment.save()

        payments_values = payments.values(
            'player__first_name',
            'player__last_name',
            'n_fact_visiting',
            'id',
            'group_name'
        ).order_by(
            'group_order',
            'player__last_name',
            'player__first_name'
        )

        users_info = have_not_paid_users_info(payments_values)
        n_lessons_info, should_pay, should_pay_balls, tarif_info, this_month_payment_info, payment_info = '', '', '',\
                                                                                                   '', '', ''
    else:
        should_pay = 0
        payments = Payment.objects.filter(player__traininggroup__id=group_id, month=month, year=year)
        for payment in payments:
            payment.save()

        check_if_players_not_in_payments(group_id, payments, year, month)

        paid_this_month = payments.aggregate(sigma=Sum('fact_amount'))
        this_month_payment_info = f'{static_text.TOTAL_PAID}: {paid_this_month["sigma"]}\n\n'

        group = TrainingGroup.objects.get(id=group_id)
        n_lessons = GroupTrainingDay.objects.filter(date__month=month, date__year=int(year)+2020, group=group,
                                                    is_available=True).count()
        n_lessons_info = f'{static_text.NUMBER_OF_TRAINS}: {n_lessons}\n'
        tarif_info = f'{static_text.TARIF}: {group.tarif_for_one_lesson}\n'
        if group.status == TrainingGroup.STATUS_GROUP:
            should_pay = n_lessons * group.tarif_for_one_lesson
        elif group.status == TrainingGroup.STATUS_SECTION:
            should_pay = TARIF_SECTION
        elif group.status == TrainingGroup.STATUS_FEW:
            should_pay = n_lessons * TARIF_FEW

        should_pay_balls = 100 * round(n_lessons / 4)
        title = f'{group.name}\n'
        help_info = static_text.FIRST_LAST_NAME_FACT_NUMBER_OF_VISITS

        payment_info = static_text.MUST_PAY_FOR_TRAINS_AND_BALLS.format(
            should_pay,
            should_pay_balls
        )

        users_info = info_about_users(payments, for_admin=True, payment=True)

    date_info = f'{from_digit_to_month[int(month)]} {int(year) + 2020}\n'

    text = f"{title}{date_info}{n_lessons_info}{tarif_info}{payment_info}\n{this_month_payment_info}" \
           f"<b>id</b>. {help_info}\n\n" \
           f"{users_info}"

    markup = keyboard_utils.change_payment_info_keyboard(
        year=year,
        month=month,
        group_id=group_id
    )

    bot_edit_message(context.bot, text, update, markup)


def change_payment_data(update, context):
    year, month, _ = update.callback_query.data[len(manage_data.PAYMENT_START_CHANGE):].split('|')
    user, _ = User.get_user_and_created(update, context)

    markup = keyboard_utils.back_to_payment_groups_when_changing_payment_keyboard(
        year=year,
        month=month,
        from_digit_to_month_dict=from_digit_to_month
    )

    base.common_for_bots.tasks.send_message(
        chat_id=user.id,
        text=static_text.TO_INSERT_PAYMENT_DATA_HELP_INFO,
        reply_markup=markup
    )

    return START_CHANGE_PAYMENT


def get_id_amount(update, context):
    user, _ = User.get_user_and_created(update, context)
    try:
        payment_id, amount = update.message.text.split(' ')
        payment_id = int(payment_id)
        amount = int(amount)
        payment = Payment.objects.select_related('player').get(id=payment_id)

        text = f'{payment.player.first_name} {payment.player.last_name}\n' \
               f'{static_text.YEAR}: {2020 + int(payment.year)}\n' \
               f'{static_text.MONTH}: {from_digit_to_month[int(payment.month)]}\n' \
               f'<b>{payment.fact_amount}₽ ➡ {amount}₽</b>'
        markup = keyboard_utils.cancel_confirm_changing_payment_info_keyboard(
            payment_id=payment_id,
            amount=amount
        )
        base.common_for_bots.tasks.send_message(
            chat_id=user.id,
            text=text,
            reply_markup=markup,
            parse_mode='HTML'
        )
    except ValueError:
        base.common_for_bots.tasks.send_message(
            chat_id=user.id,
            text=static_text.ERROR_INCORRECT_ID_OR_MONEY
        )
    except ObjectDoesNotExist:
        base.common_for_bots.tasks.send_message(
            chat_id=user.id,
            text=static_text.NO_SUCH_OBJECT_IN_DATABASE
        )

    return CONFIRM_OR_CANCEL


def confirm_or_cancel_changing_payment(update, context):
    permission, payment_id, amount = update.callback_query.data[len(manage_data.PAYMENT_CONFIRM_OR_CANCEL):].split('|')
    payment = Payment.objects.get(id=payment_id)
    if permission == 'NO':
        text = UP_TO_YOU
    else:
        payment.fact_amount = int(amount)
        payment.save()
        text = static_text.CHANGES_ARE_MADE

    markup = keyboard_utils.back_to_payment_groups_when_changing_payment_keyboard(
        year=payment.year,
        month=payment.month,
        from_digit_to_month_dict=from_digit_to_month
    )

    bot_edit_message(context.bot, text, update, markup)

    return ConversationHandler.END

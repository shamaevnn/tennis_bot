import datetime
import telegram

from .static_text import *
from django.db.models import Sum, Q, Count, ExpressionWrapper, IntegerField, F
from telegram.ext import ConversationHandler
from django.core.exceptions import ObjectDoesNotExist
from base.models import User, GroupTrainingDay, Payment, TrainingGroup, AlertsLog
from base.utils import moscow_datetime, bot_edit_message, get_time_info_from_tr_day, info_about_users, \
    clear_broadcast_messages
from tele_interface.manage_data import PERMISSION_FOR_IND_TRAIN, SHOW_GROUPDAY_INFO, \
    CLNDR_ADMIN_VIEW_SCHEDULE, CLNDR_ACTION_BACK, CLNDR_NEXT_MONTH, CLNDR_DAY, CLNDR_IGNORE, \
    CLNDR_PREV_MONTH, PAYMENT_YEAR, PAYMENT_YEAR_MONTH, PAYMENT_YEAR_MONTH_GROUP, PAYMENT_START_CHANGE, \
    PAYMENT_CONFIRM_OR_CANCEL, AMOUNT_OF_IND_TRAIN, SEND_MESSAGE
from tele_interface.static_text import from_digit_to_month
from tele_interface.utils import separate_callback_data, create_tr_days_for_future
from tele_interface.keyboard_utils import create_calendar
from tennis_bot.settings import TARIF_SECTION, TARIF_FEW
from .keyboard_utils import construct_menu_groups_for_send_message, day_buttons_coach_info, \
    construct_menu_months, construct_menu_groups, back_to_payment_groups_when_changing_payment_keyboard, \
    cancel_confirm_changing_payment_info_keyboard, change_payment_info_keyboard, choose_year_to_group_payment_keyboard, \
    back_from_show_grouptrainingday_info_keyboard, how_many_trains_to_save_keyboard, go_to_site_keyboard
from .utils import check_if_players_not_in_payments
from tennis_bot.settings import TELEGRAM_TOKEN
from datetime import date, datetime, timedelta


def permission_for_ind_train(update, context):
    permission, user_id, tr_day_id = update.callback_query.data[len(PERMISSION_FOR_IND_TRAIN):].split('|')

    player = User.objects.get(id=user_id)
    tr_day = GroupTrainingDay.objects.filter(id=tr_day_id)

    if tr_day.exists():
        tr_day = tr_day.first()
        time_tlg, _, _, date_tlg, _, _, _ = get_time_info_from_tr_day(tr_day)
        markup = None

        if permission == 'yes':
            markup = how_many_trains_to_save_keyboard(tr_day_id=tr_day_id)
            admin_text = HOW_MANY_TRAINS_TO_SAVE

            user_text = f'Отлично, тренер подтвердил тренировку <b>{date_tlg}</b>\n' \
                        f'Время: <b>{time_tlg}</b>\n' \
                        f'Не забудь!'

        else:
            admin_text = WILL_SAY_THAT_TRAIN_IS_CANCELLED.format(
                player.last_name,
                player.first_name,
                date_tlg,
                time_tlg
            )

            user_text = f'Внимание!!!\nИндивидуальная тренировка <b> {date_tlg}</b>\n' \
                        f'в <b>{time_tlg}</b>\n' \
                        f'<b>ОТМЕНЕНА</b>'

            tr_day.delete()

        tennis_bot = telegram.Bot(TELEGRAM_TOKEN)
        tennis_bot.send_message(
            player.id,
            user_text,
            parse_mode='HTML'
        )

    else:
        admin_text = TRAIN_IS_ALREADY_CANCELLED
        markup = None

    bot_edit_message(context.bot, admin_text, update, markup=markup)


def save_many_ind_trains(update, context):
    tr_day_id, num_lessons = update.callback_query.data[len(AMOUNT_OF_IND_TRAIN):].split("|")
    tr_day = GroupTrainingDay.objects.get(id=tr_day_id)

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
    text = WISH_GOOD_TRAIN.format(
        date_tlg,
        day_of_week,
        time_tlg
    )
    if num_lessons == 'one':
        text += SAVED_ONCE
    else:
        create_tr_days_for_future(tr_day)
        text += SAVED_2_MONTHS_AHEAD

    bot_edit_message(context.bot, text, update)


def admin_calendar_selection(bot, update):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    """
    query = update.callback_query
    (purpose, action, year, month, day) = separate_callback_data(query.data)
    curr = date(int(year), int(month), 1)

    if action == CLNDR_IGNORE:
        bot.answer_callback_query(callback_query_id=query.id)
    elif action == CLNDR_DAY:
        bot_edit_message(bot, query.message.text, update)
        return True, purpose, date(int(year), int(month), int(day))
    elif action == CLNDR_PREV_MONTH:
        pre = curr - timedelta(days=1)
        bot_edit_message(bot, query.message.text, update, create_calendar(purpose, int(pre.year), int(pre.month)))
    elif action == CLNDR_NEXT_MONTH:
        ne = curr + timedelta(days=31)
        bot_edit_message(bot, query.message.text, update, create_calendar(purpose, int(ne.year), int(ne.month)))
    elif action == CLNDR_ACTION_BACK:
        if purpose == CLNDR_ADMIN_VIEW_SCHEDULE:
            text = TRAIN_DAYS
        else:
            text = TRAIN_DAYS
        bot_edit_message(bot, text, update, create_calendar(purpose, int(year), int(month)))
    else:
        bot.answer_callback_query(callback_query_id=query.id, text="Something went wrong!")
    return False, purpose, []


def inline_calendar_handler(update, context):
    selected, purpose, date_my = admin_calendar_selection(context.bot, update)
    if selected:
        if purpose == CLNDR_ADMIN_VIEW_SCHEDULE:
            tr_days = GroupTrainingDay.objects.filter(date=date_my).select_related('group').order_by('start_time')
            if tr_days.count():
                markup = day_buttons_coach_info(tr_days, SHOW_GROUPDAY_INFO)
                _, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_days.first())
                text = '📅{} ({})'.format(date_tlg, day_of_week)
            else:
                text = NO_TRAINS_THIS_DAY
                markup = create_calendar(purpose, date_my.year, date_my.month)
            bot_edit_message(context.bot, text, update, markup)


def show_coach_schedule(update, context):
    update.message.reply_text(
        text=TRAIN_DAYS,
        reply_markup=create_calendar(CLNDR_ADMIN_VIEW_SCHEDULE)
    )


def redirect_to_site(update, context):
    markup = go_to_site_keyboard()
    update.message.reply_text(
        text=ADMIN_SITE,
        reply_markup=markup
    )


GROUP_IDS, TEXT_TO_SEND = 2, 3


def select_groups_where_should_send(update, context):
    text = WHOM_TO_SEND_TO

    banda_groups = TrainingGroup.objects.filter(status=TrainingGroup.STATUS_GROUP, max_players__gt=1).order_by('order')

    if update.callback_query:
        group_ids = update.callback_query.data[len(SEND_MESSAGE):].split("|")
        markup = construct_menu_groups_for_send_message(banda_groups, f'{update.callback_query.data}')

        if len(group_ids) == 2 and group_ids[-1] == '-1':
            # ['', '-1'] -- just pressed confirm
            text = CHOOSE_GROUP_AFTER_THAT_CONFIRM
        bot_edit_message(context.bot, text, update, markup)
        return GROUP_IDS

    else:
        markup = construct_menu_groups_for_send_message(banda_groups, f'{SEND_MESSAGE}')
        update.message.reply_text(
            text=text,
            reply_markup=markup
        )


def text_to_send(update, context):
    group_ids = update.callback_query.data[len(SEND_MESSAGE):].split("|")
    group_ids.remove('')
    if group_ids[-1] == '-1':  # if pressed "confirm"
        list_of_group_ids = list(set([int(x) for x in group_ids if x]))
        if 0 in list_of_group_ids:
            # pressed 'send to all groups'
            text = SENDING_TO_ALL_GROUPS_TYPE_TEXT

            banda_groups = TrainingGroup.objects.filter(status=TrainingGroup.STATUS_GROUP,
                                                        max_players__gt=1).distinct()
            players = User.objects.filter(traininggroup__in=banda_groups).distinct()

        elif -2 in list_of_group_ids:
            # pressed 'send to all'
            text = WILL_SEND_TO_ALL_TYPE_TEXT
            players = User.objects.filter(status__in=[User.STATUS_TRAINING,
                                                      User.STATUS_ARBITRARY,
                                                      User.STATUS_IND_TRAIN])
        else:
            text = WILL_SEND_TO_THE_FOLLOWING_GROUPS

            group_names = "\n".join(list(TrainingGroup.objects.filter(id__in=list_of_group_ids).values_list('name', flat=True)))
            text += group_names
            text += TYPE_TEXT_OF_MESSAGE

            players = User.objects.filter(traininggroup__in=list_of_group_ids).distinct()

        objs = [AlertsLog(player=player, alert_type=AlertsLog.CUSTOM_COACH_MESSAGE) for player in players]
        AlertsLog.objects.bulk_create(objs)

        text += OR_PRESS_CANCEL
        bot_edit_message(context.bot, text, update)

        return TEXT_TO_SEND

    else:
        select_groups_where_should_send(update, context)


def receive_text_and_send(update, context):
    text = update.message.text

    if text == CANCEL:
        return ConversationHandler.END

    else:
        alert_instances = AlertsLog.objects.filter(
            is_sent=False,
            tr_day__isnull=True,
            alert_type=AlertsLog.CUSTOM_COACH_MESSAGE,
            info__isnull=True
        ).distinct()
        player_ids = list(alert_instances.values_list('player', flat=True))

        clear_broadcast_messages(
            user_ids=player_ids,
            message=text
        )

        alert_instances.update(is_sent=True, info=text)

        update.message.reply_text(
            text=IS_SENT
        )

        return ConversationHandler.END


def show_traingroupday_info(update, context):
    tr_day_id = update.callback_query.data[len(SHOW_GROUPDAY_INFO):]
    tr_day = GroupTrainingDay.objects.select_related('group').get(id=tr_day_id)

    availability = f'{NO_TRAIN}\n' if not tr_day.is_available else ''
    is_individual = f'{INDIVIDUAL_TRAIN}\n' if tr_day.is_individual else f'{GROUP_TRAIN}️\n'
    affiliation = f'{MY_TRAIN}\n\n' if tr_day.tr_day_status == GroupTrainingDay.MY_TRAIN_STATUS else f'{RENT}\n\n'

    group_name = f"{tr_day.group.name}\n"

    if not tr_day.is_individual:
        group_players = f'{PLAYERS_FROM_GROUP}:\n{info_about_users(tr_day.group.users.all().difference(tr_day.absent.all()), for_admin=True)}\n'
        visitors = f'\n{HAVE_COME_FROM_OTHERS}:\n{info_about_users(tr_day.visitors, for_admin=True)}\n' if tr_day.visitors.count() else ''
        pay_visitors = f'\n{HAVE_COME_FOR_MONEY}:\n{info_about_users(tr_day.pay_visitors, for_admin=True)}\n' if tr_day.pay_visitors.count() else ''
        absents = f'\n{ARE_ABSENT}:\n{info_about_users(tr_day.absent, for_admin=True)}\n' if tr_day.absent.count() else ''
    else:
        group_players = ''
        visitors = ''
        pay_visitors = ''
        absents = ''

    time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)

    general_info = f'<b>{date_tlg} ({day_of_week})\n{time_tlg}</b>' + '\n' + availability + is_individual + affiliation
    users_info = group_name + group_players + visitors + pay_visitors + absents
    text = general_info + users_info

    markup = back_from_show_grouptrainingday_info_keyboard(
        year=tr_day.date.year,
        month=tr_day.date.month,
        day=tr_day.date.day
    )

    bot_edit_message(context.bot, text, update, markup)


def start_payment(update, context):
    text = CHOOSE_YEAR
    now_date = moscow_datetime(datetime.now()).date()
    markup = choose_year_to_group_payment_keyboard(
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
    year = update.callback_query.data[len(PAYMENT_YEAR):]
    text = CHOOSE_MONTH
    markup = construct_menu_months(Payment.MONTHS, f'{PAYMENT_YEAR_MONTH}{year}|')
    bot_edit_message(context.bot, text, update, markup)


def month_payment(update, context):
    year, month = update.callback_query.data[len(PAYMENT_YEAR_MONTH):].split('|')

    amount_for_this_month = Payment.objects.filter(year=year, month=month).aggregate(sigma=Sum('fact_amount'))

    should_pay_this_month = TrainingGroup.objects.annotate(count_tr_days=Count('grouptrainingday',
                                                                               filter=Q(
                                                                                   grouptrainingday__is_available=True,
                                                                                   grouptrainingday__date__month=month,
                                                                                   grouptrainingday__date__year=int(
                                                                                       year) + 2020),
                                                                               distinct=True),
                                                           count_users=Count('users', distinct=True)).filter(
        max_players__gt=1).annotate(should_pay=ExpressionWrapper(F('count_users') *
                                                                 F('tarif_for_one_lesson') * F('count_tr_days'),
                                                                 output_field=IntegerField())).aggregate(sigma=Sum('should_pay'))

    text = f'{int(year) + 2020}--{from_digit_to_month[int(month)]}\n' \
           f'<b>{TOTAL_PAID}: {amount_for_this_month["sigma"] if amount_for_this_month["sigma"] else 0}</b>\n' \
           f'<b>{MUST_PAY}: {should_pay_this_month["sigma"]}</b>\n' \
           f'{CHOOSE_GROUP}'

    banda_groups = TrainingGroup.objects.filter(name__iregex=r'БАНДА').order_by('order')
    markup = construct_menu_groups(banda_groups, f'{PAYMENT_YEAR_MONTH_GROUP}{year}|{month}|')
    bot_edit_message(context.bot, text, update, markup)

    return ConversationHandler.END


def group_payment(update, context):
    year, month, group_id = update.callback_query.data[len(PAYMENT_YEAR_MONTH_GROUP):].split('|')

    if int(group_id) == 0:
        title = f'{REST}\n'
        payments = Payment.objects.filter(player__status__in=[User.STATUS_TRAINING, User.STATUS_ARBITRARY],
                                          month=month,
                                          year=year).exclude(player__traininggroup__name__iregex='БАНДА')
        paid_this_month = payments.aggregate(sigma=Sum('fact_amount'))
        n_lessons_info, should_pay, should_pay_balls, tarif_info = '', '', '', ''
    else:
        should_pay = 0
        payments = Payment.objects.filter(player__traininggroup__id=group_id, month=month, year=year)
        check_if_players_not_in_payments(group_id, payments, year, month)
        paid_this_month = payments.aggregate(sigma=Sum('fact_amount'))
        group = TrainingGroup.objects.get(id=group_id)
        n_lessons = GroupTrainingDay.objects.filter(date__month=month, date__year=int(year)+2020, group=group,
                                                    is_available=True).count()
        n_lessons_info = f'{NUMBER_OF_TRAINS}: {n_lessons}\n'
        tarif_info = f'{TARIF}: {group.tarif_for_one_lesson}\n'
        if group.status == TrainingGroup.STATUS_GROUP:
            should_pay = n_lessons * group.tarif_for_one_lesson
        elif group.status == TrainingGroup.STATUS_SECTION:
            should_pay = TARIF_SECTION
        elif group.status == TrainingGroup.STATUS_FEW:
            should_pay = n_lessons * TARIF_FEW

        should_pay_balls = 100 * round(n_lessons / 4)
        title = f'{group.name}\n'

    for payment in payments:
        payment.save()

    date_info = f'{from_digit_to_month[int(month)]} {int(year) + 2020}\n'
    payment_info = MUST_PAY_FOR_TRAINS_AND_BALLS.format(
        should_pay,
        should_pay_balls
    )
    this_month_payment_info = f'{TOTAL_PAID}: {paid_this_month["sigma"]}\n\n'
    text = f"{title}{date_info}{n_lessons_info}{tarif_info}{payment_info}{this_month_payment_info}" \
           f"<b>id</b>. {FIRST_LAST_NAME_FACT_NUMBER_OF_VISITS}\n\n" \
           f"{info_about_users(payments, for_admin=True, payment=True)}"

    markup = change_payment_info_keyboard(
        year=year,
        month=month,
        group_id=group_id
    )

    bot_edit_message(context.bot, text, update, markup)


START_CHANGE_PAYMENT, CONFIRM_OR_CANCEL = range(2)


def change_payment_data(update, context):
    year, month, _ = update.callback_query.data[len(PAYMENT_START_CHANGE):].split('|')
    text = TO_INSERT_PAYMENT_DATA_HELP_INFO
    user, _ = User.get_user_and_created(update, context)

    markup = back_to_payment_groups_when_changing_payment_keyboard(
        year=year,
        month=month,
        from_digit_to_month_dict=from_digit_to_month
    )

    context.bot.send_message(
        chat_id=user.id,
        text=text,
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
               f'{YEAR}: {2020 + int(payment.year)}\n' \
               f'{MONTH}: {from_digit_to_month[int(payment.month)]}\n' \
               f'<b>{payment.fact_amount}₽ ➡ {amount}₽</b>'
        markup = cancel_confirm_changing_payment_info_keyboard(
            payment_id=payment_id,
            amount=amount
        )
        context.bot.send_message(
            chat_id=user.id,
            text=text,
            reply_markup=markup,
            parse_mode='HTML'
        )

    except ValueError:
        text = ERROR_INCORRECT_ID_OR_MONEY
        context.bot.send_message(
            chat_id=user.id,
            text=text
        )

    except ObjectDoesNotExist:
        text = NO_SUCH_OBJECT_IN_DATABASE
        context.bot.send_message(
            chat_id=user.id,
            text=text
        )

    return CONFIRM_OR_CANCEL


def confirm_or_cancel_changing_payment(update, context):
    permission, payment_id, amount = update.callback_query.data[len(PAYMENT_CONFIRM_OR_CANCEL):].split('|')
    payment = Payment.objects.get(id=payment_id)
    if permission == 'NO':
        text = UP_TO_YOU
    else:
        payment.fact_amount = int(amount)
        payment.save()

        text = CHANGES_ARE_MADE

    markup = back_to_payment_groups_when_changing_payment_keyboard(
        year=payment.year,
        month=payment.month,
        from_digit_to_month_dict=from_digit_to_month
    )

    bot_edit_message(context.bot, text, update, markup)

    return ConversationHandler.END

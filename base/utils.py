import calendar
from datetime import date

import telegram
import datetime

from django.db.models import F
from pytz import timezone
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

from tele_interface.manage_data import SEND_MESSAGE
from tele_interface.static_text import from_eng_to_rus_day_week, CANCEL_TRAIN_PLUS_BONUS_LESSON_2, \
    TRAIN_IS_AVAIABLE_CONGRATS, NO_PAYMENT_BUTTON, MY_DATA_BUTTON, HELP_BUTTON, SKIP_LESSON_BUTTON, TAKE_LESSON_BUTTON
from tennis_bot.settings import TELEGRAM_TOKEN, DEBUG

DTTM_BOT_FORMAT = '%Y.%m.%d.%H.%M'
DT_BOT_FORMAT = '%Y.%m.%d'
TM_HOUR_BOT_FORMAT = '%H'
TM_DAY_BOT_FORMAT = '%d'
TM_TIME_SCHEDULE_FORMAT = '%H:%M'


def send_message(user_id, text, reply_markup=None, tg_token=TELEGRAM_TOKEN, parse_mode='HTML'):
    bot = telegram.Bot(tg_token)
    try:
        if not DEBUG:
            if reply_markup is not None:
                if reply_markup.get('inline_keyboard'):
                    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(**button)
                                                          for button in reply_markup.get('inline_keyboard')[0]]])

        m = bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )
    except telegram.error.Unauthorized:
        from base.models import User
        print(f"Can't send message to {user_id}. Reason: Bot was stopped.")
        User.objects.filter(id=user_id).update(is_blocked=True)
        success = False
    except Exception as e:
        print(f"Can't send message to {user_id}. Reason: {e}")
        success = False
    else:
        success = True
        from base.models import User
        User.objects.filter(id=user_id).update(is_blocked=False)
    return success


def clear_broadcast_messages(user_ids, message, reply_markup=None, tg_token=TELEGRAM_TOKEN, sleep_between=0.4, parse_mode="HTML"):
    from base.tasks import broadcast_message
    if DEBUG:
        broadcast_message(
            user_ids=user_ids,
            message=message,
            reply_markup=reply_markup,
            tg_token=tg_token,
            sleep_between=sleep_between,
            parse_mode=parse_mode
        )
    else:
        broadcast_message.delay(
            user_ids=user_ids,
            message=message,
            reply_markup=reply_markup.to_dict() if reply_markup else None,
            tg_token=tg_token,
            sleep_between=sleep_between,
            parse_mode=parse_mode
        )


def get_players_for_tr_day(tr_day):
    group_members = tr_day.group.users.all()
    visitors = tr_day.visitors.all()
    pay_visitors = tr_day.visitors.all()
    pay_bonus_visitors = tr_day.pay_bonus_visitors.all()
    return group_members.union(visitors, pay_visitors, pay_bonus_visitors)


def get_actual_players_without_absent(tr_day):
    return get_players_for_tr_day(tr_day).difference(tr_day.absent.all())


def send_alert_about_changing_tr_day_status(tr_day, new_is_available):
    if not new_is_available:
        text = CANCEL_TRAIN_PLUS_BONUS_LESSON_2.format(tr_day.date, tr_day.start_time)
        users = get_actual_players_without_absent(tr_day)
        users.update(bonus_lesson=F('bonus_lesson') + 1)
    else:
        text = TRAIN_IS_AVAIABLE_CONGRATS.format(tr_day.date, tr_day.start_time)

    clear_broadcast_messages(
        user_ids=list(get_players_for_tr_day(tr_day).values_list('id', flat=True)),
        message=text,
        reply_markup=construct_main_menu()
    )


def send_alert_about_changing_tr_day_time(tr_day, text):
    absents = tr_day.absent.all()
    clear_broadcast_messages(
        user_ids=list(get_players_for_tr_day(tr_day).union(absents).values_list('id', flat=True)),
        message=text,
        reply_markup=construct_main_menu()
    )


def moscow_datetime(date_time):
    return date_time.astimezone(timezone('Europe/Moscow')).replace(tzinfo=None)


def bot_edit_message(bot, text, update, markup=None):
    bot.edit_message_text(text=text,
                          chat_id=update.callback_query.message.chat_id,
                          message_id=update.callback_query.message.message_id,
                          parse_mode='HTML',
                          reply_markup=markup)


def extract_user_data_from_update(update):
    """ python-telegram-bot's Update instance --> User info """
    if update.message is not None:
        user = update.message.from_user.to_dict()
    elif update.inline_query is not None:
        user = update.inline_query.from_user.to_dict()
    elif update.chosen_inline_result is not None:
        user = update.chosen_inline_result.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.from_user is not None:
        user = update.callback_query.from_user.to_dict()
    elif update.callback_query is not None and update.callback_query.message is not None:
        user = update.callback_query.message.chat.to_dict()
    else:
        raise Exception(f"Can't extract user data from update: {update}")

    return dict(
        id=user["id"],
        is_blocked=False,
        **{
            k: user[k]
            for k in ["username", "first_name", "last_name"]
            if k in user and user[k] is not None
        },
    )


def get_time_info_from_tr_day(tr_day):
    """
    :param tr_day: instance of GroupTrainingDay
    :return: end_time, start_time: datetime,
             *time_tlg: str, is used in buttons,
             day_of_week: str, russian name of day of week
    """
    start_time = tr_day.start_time
    start_time_tlg = start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
    end_time = datetime.datetime.combine(tr_day.date, start_time) + tr_day.duration
    end_time_tlg = end_time.strftime(TM_TIME_SCHEDULE_FORMAT)
    time_tlg = f'{start_time_tlg} — {end_time_tlg}'
    day_of_week = from_eng_to_rus_day_week[calendar.day_name[tr_day.date.weekday()]]
    date_tlg = tr_day.date.strftime(DT_BOT_FORMAT)

    return time_tlg, start_time_tlg, end_time_tlg, date_tlg, day_of_week, start_time, end_time


def handle_selecting_groups_to_send_message_to(ids_counter, group_ids, group_id, button_data_text, button_text):
    if group_id not in group_ids:
        text = button_text
    elif ids_counter[group_id] > 1 and ids_counter[group_id] % 2 == 0:
        text = button_text
        group_ids.remove(group_id)
        group_ids.remove(group_id)
        button_data_text = button_data_text[:len(SEND_MESSAGE)] + "|".join(group_ids)
    else:
        text = f'{button_text} ✅'

    return text, button_data_text


def have_not_paid_users_info(payments_values):
    return '\n'.join(
        (
            f"<b>{x['id']}</b>. {x['player__last_name']} {x['player__first_name']} -- {x['n_fact_visiting']} ({x['group_name']})"
            for x in payments_values
        )
    )


def info_about_users(users, for_admin=False, payment=False):
    """
    :param payment: info about payment or not
    :param for_admin: show info for admin or not (number instead of smile)
    :param users: User instance
    :return: (first_name + last_name + \n){1,} -- str
    """
    if for_admin:
        if payment:
            return '\n'.join(
                (f"<b>{x['id']}</b>. {x['player__last_name']} {x['player__first_name']} -- {x['fact_amount']}₽, {x['n_fact_visiting']}"
                    for x in users.values(
                        'player__first_name',
                        'player__last_name',
                        'fact_amount',
                        'n_fact_visiting',
                        'id'
                    ).order_by(
                        'player__last_name',
                        'player__first_name'
                    )
                )
            )
        else:
            return '\n'.join(
                (f"{i + 1}. {x['last_name']} {x['first_name']}" for i, x in enumerate(users.values('first_name',
                                                                                                   'last_name').order_by('last_name'))))
    else:
        return '\n'.join(
            (f"👤{x['last_name']} {x['first_name']}" for x in
             users.values('first_name', 'last_name').order_by('last_name')))


def construct_main_menu(user=None, user_status=None):
    payment_button = []
    from base.models import User
    if user and user_status == User.STATUS_TRAINING:
        from base.models import Payment
        today_date = date.today()
        user_payment = Payment.objects.filter(player=user, player__status=user_status, fact_amount=0,
                                              year=today_date.year-2020, month=today_date.month)
        if user_payment.exists():
            payment_button = [NO_PAYMENT_BUTTON]

    return ReplyKeyboardMarkup([
        payment_button,
        [MY_DATA_BUTTON, HELP_BUTTON],
        [SKIP_LESSON_BUTTON, TAKE_LESSON_BUTTON]],
        resize_keyboard=True)
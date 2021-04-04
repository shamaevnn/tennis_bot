import os
import django
import random
import pytz
import time


import telegram
from tennis_bot.celery import app
from celery.utils.log import get_task_logger
from django.db.models import ExpressionWrapper, F, DurationField
from base.models import AlertsLog, GroupTrainingDay, Payment, User
from base.utils import moscow_datetime, get_time_info_from_tr_day, send_message
from datetime import datetime, timedelta
from tennis_bot.settings import TELEGRAM_TOKEN
from tele_interface.static_text import ALERT_TEXTS, from_digit_to_month

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()

utc=pytz.UTC

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def broadcast_message(user_ids, message, reply_markup=None, tg_token=TELEGRAM_TOKEN, sleep_between=0.4, parse_mode="HTML"):
    """ It's used to broadcast message to big amount of users """
    logger.info(f"Going to send message: '{message}' to {len(user_ids)} users")

    for user_id in user_ids:
        try:
            send_message(
                user_id=user_id,
                text=message,
                reply_markup=reply_markup,
                parse_mode=parse_mode,
                tg_token=tg_token,
            )
            logger.info(f"Broadcast message was sent to {user_id}")
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}, reason: {e}" )
        time.sleep(max(sleep_between, 0.1))

    logger.info("Broadcast finished!")


@app.task(ignore_result=True)
def send_alert_about_coming_train():
    # смотрим на те тренировки, по которым уже отправили сообщение
    alert_log_tr_days = list(AlertsLog.objects.filter(
        is_sent=True, alert_type=AlertsLog.COMING_TRAIN).values_list("tr_day_id", flat=True).distinct())
    # выбираем предстоящие тренировки, исключаем выше описанные
    tr_days = GroupTrainingDay.objects.annotate(
        diff=ExpressionWrapper(F('start_time') + F('date') - moscow_datetime(datetime.now()),
                               output_field=DurationField()),
        train_dttm=ExpressionWrapper(F('start_time') + F('date'),
                                     output_field=DurationField())).filter(train_dttm__gte=moscow_datetime(datetime.now()),
                                                                           diff__lte=timedelta(hours=5),
                                                                           is_available=True).exclude(id__in=alert_log_tr_days).distinct()

    for tr_day in tr_days:
        group_members = tr_day.group.users.all()
        visitors = tr_day.visitors.all()
        players = group_members.union(visitors).difference(tr_day.absent.all())

        bot = telegram.Bot(TELEGRAM_TOKEN)
        for player in players:
            alert_dict = random.choice(ALERT_TEXTS)
            text_alert = list(alert_dict.keys())[0]
            photo_url = alert_dict[text_alert]

            time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
            dttm_train_info = f'📅Дата: <b>{date_tlg} ({day_of_week})</b>\n' \
                              f'⏰Время: <b>{time_tlg}</b>\n\n'

            text_alert += dttm_train_info

            try:
                bot.send_photo(player.id,
                               photo=photo_url,
                               caption=text_alert,
                               parse_mode='HTML')
                AlertsLog.objects.create(is_sent=True, player=player, tr_day=tr_day, alert_type=AlertsLog.COMING_TRAIN)
            except (telegram.error.Unauthorized, telegram.error.BadRequest) as e:
                AlertsLog.objects.create(is_sent=False, player=player, tr_day=tr_day, alert_type=AlertsLog.COMING_TRAIN,
                                         info=e + '\n\n' + photo_url)


@app.task(ignore_result=True)
def send_alert_about_payment():
    now_day = moscow_datetime(datetime.now())
    # отправляем в первые 2 дня месяца
    if now_day.day <= 2:
        not_paid = Payment.objects.filter(
                             fact_amount=0,
                             player__status=User.STATUS_TRAINING,
                             year=str(now_day.year - 2020),
                             month=str(now_day.month)).exclude(
                                        alertslog__is_sent=True,
                                        alertslog__alert_type=AlertsLog.SHOULD_PAY,
                                        alertslog__dttm_sent__gt=(datetime.now() + timedelta(hours=-7)).replace(tzinfo=utc)).distinct(
                                                                                ).select_related('player')

        month = from_digit_to_month[int(now_day.month)].lower()
        bot = telegram.Bot(TELEGRAM_TOKEN)
        for payment in not_paid:
            text = f'{payment.player.first_name}, нужно заплатить за {month}. Сумму можно узнать по кнопке "Мои данные".'
            try:
                bot.send_message(payment.player_id,
                                 text)
                AlertsLog.objects.create(is_sent=True, payment=payment, alert_type=AlertsLog.SHOULD_PAY)
            except (telegram.error.Unauthorized, telegram.error.BadRequest) as e:
                AlertsLog.objects.create(is_sent=False, payment=payment, alert_type=AlertsLog.COMING_TRAIN, info=e)


# schedule.every(59).minutes.do(send_alert_about_coming_train)
# schedule.every().day.at("19:00").do(send_alert_about_payment)
# schedule.every().day.at("10:00").do(send_alert_about_payment)
#
# while 1:
#     schedule.run_pending()


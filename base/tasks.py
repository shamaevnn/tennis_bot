import os
import django
import random
import pytz

import telegram
from tennis_bot.celery import app
from celery.utils.log import get_task_logger
from django.db.models import ExpressionWrapper, F, DurationField
from base.models import AlertsLog, GroupTrainingDay, Payment, User, Photo
from base.common_for_bots.utils import get_actual_players_without_absent, moscow_datetime, \
    get_time_info_from_tr_day
from datetime import datetime, timedelta
from tennis_bot.settings import TELEGRAM_TOKEN
from player_bot.user_info.static_text import MY_DATA_BUTTON
from base.common_for_bots.static_text import from_digit_to_month

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()

utc=pytz.UTC

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def send_alert_about_coming_train():
    # смотрим на те тренировки, по которым уже отправили сообщение
    alert_log_tr_days = list(AlertsLog.objects.filter(
        is_sent=True, alert_type=AlertsLog.COMING_TRAIN).values_list("tr_day_id", flat=True).distinct())
    # выбираем предстоящие тренировки, исключаем выше описанные
    tr_days = GroupTrainingDay.objects.select_related('group').annotate(
        diff=ExpressionWrapper(
            F('start_time') + F('date') - moscow_datetime(datetime.now()), output_field=DurationField()
        ),
        train_dttm=ExpressionWrapper(
            F('start_time') + F('date'), output_field=DurationField())
    ).filter(
        train_dttm__gte=moscow_datetime(datetime.now()),
        diff__lte=timedelta(hours=5),
        is_available=True
    ).exclude(
        id__in=alert_log_tr_days
    ).distinct()

    photo_ids = list(Photo.objects.values_list('id', flat=True))

    for tr_day in tr_days:
        players = get_actual_players_without_absent(tr_day)

        bot = telegram.Bot(TELEGRAM_TOKEN)
        for player in players:
            photo_id = random.choice(photo_ids)
            photo = Photo.objects.get(id=photo_id)
            telegram_id_exists = photo.check_if_telegram_id_is_present()
            if not telegram_id_exists:
                photo.save_telegram_id()

            time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(tr_day)
            dttm_train_info = f'📅Дата: <b>{date_tlg} ({day_of_week})</b>\n' \
                              f'⏰Время: <b>{time_tlg}</b>\n\n'

            text_alert = f'{photo.text}\n{dttm_train_info}'

            try:
                bot.send_photo(player.id,
                               photo=photo.telegram_id,
                               caption=text_alert,
                               parse_mode='HTML')
                AlertsLog.objects.create(is_sent=True, player=player, tr_day=tr_day, alert_type=AlertsLog.COMING_TRAIN)
            except (telegram.error.Unauthorized, telegram.error.BadRequest) as e:
                AlertsLog.objects.create(is_sent=False, player=player, tr_day=tr_day, alert_type=AlertsLog.COMING_TRAIN,
                                         info=str(e) + '\n\n' + photo.telegram_id)


@app.task(ignore_result=True)
def send_alert_about_payment():
    now_day = moscow_datetime(datetime.now())

    not_paid = Payment.objects.filter(
                         fact_amount=0,
                         player__status=User.STATUS_TRAINING,
                         year=str(now_day.year - 2020),
                         month=str(now_day.month)
    ).exclude(
        alertslog__is_sent=True,
        alertslog__alert_type=AlertsLog.SHOULD_PAY,
        alertslog__dttm_sent__gt=(datetime.now() + timedelta(hours=-11)).replace(tzinfo=utc)
    ).distinct().select_related('player')

    month = from_digit_to_month[int(now_day.month)].lower()
    bot = telegram.Bot(TELEGRAM_TOKEN)
    for payment in not_paid:
        text = f'{payment.player.first_name}, нужно заплатить за {month}. Сумму можно узнать по кнопке "{MY_DATA_BUTTON}".'
        try:
            bot.send_message(payment.player_id,
                             text)
            AlertsLog.objects.create(is_sent=True, payment=payment, alert_type=AlertsLog.SHOULD_PAY)
        except (telegram.error.Unauthorized, telegram.error.BadRequest) as e:
            AlertsLog.objects.create(is_sent=False, payment=payment, alert_type=AlertsLog.SHOULD_PAY, info=str(e))


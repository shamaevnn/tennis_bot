import os
import traceback

import django
import pytz

import telegram

from base.redis.coming_train_alerts import SentTrDaysAlerts
from tennis_bot.celery import app
from celery.utils.log import get_task_logger
from base.models import AlertsLog, GroupTrainingDay, Payment, Player, Photo
from base.common_for_bots.utils import (
    get_actual_players_without_absent,
    moscow_datetime,
    get_time_info_from_tr_day,
)
from datetime import datetime, timedelta
from tennis_bot.settings import TELEGRAM_TOKEN, ADMIN_CHAT_ID
from player_bot.player_info.static_text import MY_DATA_BUTTON
from base.common_for_bots.static_text import from_digit_to_month, DATE_INFO

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tennis_bot.settings")
django.setup()

utc = pytz.UTC

logger = get_task_logger(__name__)


@app.task(ignore_result=True)
def send_alert_about_coming_train():
    # выбираем предстоящие тренировки, исключаем выше описанные
    tr_days = GroupTrainingDay.get_tr_days_for_alerting_about_coming_train()
    photos = Photo.objects.all()

    bot = telegram.Bot(TELEGRAM_TOKEN)
    try:
        for tr_day in tr_days:
            for player in get_actual_players_without_absent(tr_day):
                already_sent_alert_for_player = SentTrDaysAlerts.get(
                    tr_day_id=tr_day.id, player_id=player.id
                )
                if already_sent_alert_for_player:
                    continue

                time_tlg, _, _, date_tlg, day_of_week, _, _ = get_time_info_from_tr_day(
                    tr_day
                )
                date_info = DATE_INFO.format(date_tlg, day_of_week, time_tlg)

                photo = Photo.get_random_photo(photos)
                text_alert = f"{photo.text}\n{date_info}"

                success = photo.send_to_player(
                    chat_id=player.tg_id, text=text_alert, bot=bot
                )
                if success:
                    SentTrDaysAlerts.put(tr_day_id=tr_day.id, player_id=player.id)
    except Exception as e:
        text = f"Exception while sending alert about training: {e} \n {traceback.format_exc()}"
        bot.send_message(text=text, chat_id=ADMIN_CHAT_ID)


@app.task(ignore_result=True)
def send_alert_about_payment():
    now_day = moscow_datetime(datetime.now())

    not_paid = (
        Payment.objects.filter(
            fact_amount=0,
            player__status=Player.STATUS_TRAINING,
            year=str(now_day.year - 2020),
            month=str(now_day.month),
        )
        .exclude(
            alertslog__is_sent=True,
            alertslog__alert_type=AlertsLog.SHOULD_PAY,
            alertslog__dttm_sent__gt=(datetime.now() + timedelta(hours=-11)).replace(
                tzinfo=utc
            ),
        )
        .distinct()
        .select_related("player")
    )

    month = from_digit_to_month[int(now_day.month)].lower()
    bot = telegram.Bot(TELEGRAM_TOKEN)
    for payment in not_paid:
        text = f'{payment.player.first_name}, нужно заплатить за {month}. Сумму можно узнать по кнопке "{MY_DATA_BUTTON}".'
        try:
            bot.send_message(payment.player.tg_id, text)
            AlertsLog.objects.create(
                is_sent=True, payment=payment, alert_type=AlertsLog.SHOULD_PAY
            )
        except (telegram.error.Unauthorized, telegram.error.BadRequest) as e:
            AlertsLog.objects.create(
                is_sent=False,
                payment=payment,
                alert_type=AlertsLog.SHOULD_PAY,
                info=str(e),
            )

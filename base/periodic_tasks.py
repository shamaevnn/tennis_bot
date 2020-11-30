import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()

from django.db.models import ExpressionWrapper, F, DurationField
from base.models import AlertsLog, GroupTrainingDay
from base.utils import moscow_datetime, send_message, get_time_info_from_tr_day
from datetime import datetime, timedelta
from tennis_bot.config import TELEGRAM_TOKEN
from tele_interface.manage_data import ALERT_TEXTS
import schedule
import telegram
import random


def send_alert_about_coming_train():
    alert_log_tr_days = list(AlertsLog.objects.filter(
        is_sent=True, alert_type=AlertsLog.COMING_TRAIN).values_list("tr_day_id", flat=True).distinct())

    tr_days = GroupTrainingDay.objects.annotate(diff=ExpressionWrapper(
        F('start_time') + F('date') - moscow_datetime(datetime.now()),
        output_field=DurationField())).filter(date__gte=moscow_datetime(datetime.now()),
                                              diff__lte=timedelta(hours=5)).exclude(id__in=alert_log_tr_days).distinct()

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
            except (telegram.error.Unauthorized, telegram.error.BadRequest):
                player.is_blocked = True
                player.status = 'F'
                player.save()
                AlertsLog.objects.create(is_sent=False, player=player, tr_day=tr_day, alert_type=AlertsLog.COMING_TRAIN)


schedule.every(2).seconds.do(send_alert_about_coming_train)

while 1:
    schedule.run_pending()


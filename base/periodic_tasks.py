import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tennis_bot.settings')
django.setup()

from django.db.models import ExpressionWrapper, F, DurationField
from base.models import AlertsLog, GroupTrainingDay, Payment, User
from base.utils import moscow_datetime, get_time_info_from_tr_day
from datetime import datetime, timedelta
from tennis_bot.config import TELEGRAM_TOKEN
from tele_interface.manage_data import ALERT_TEXTS, from_digit_to_month
import schedule
import telegram
import random
import pytz

utc=pytz.UTC


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


schedule.every(59).minutes.do(send_alert_about_coming_train)
schedule.every().day.at("19:00").do(send_alert_about_payment)
schedule.every().day.at("10:00").do(send_alert_about_payment)

while 1:
    schedule.run_pending()


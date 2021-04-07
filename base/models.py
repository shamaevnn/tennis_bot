import calendar
import re
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django import forms
from django.utils.safestring import mark_safe
from django.db.models import Q, F, Case, When, Sum, IntegerField, ExpressionWrapper, DateTimeField, Count
from django.utils import timezone
from datetime import datetime, date, timedelta

from base.utils import moscow_datetime, TM_TIME_SCHEDULE_FORMAT, DT_BOT_FORMAT, \
    send_alert_about_changing_tr_day_time, extract_user_data_from_update, clear_broadcast_messages, construct_main_menu
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from base.utils import send_alert_about_changing_tr_day_status
from tele_interface.static_text import *
from tennis_bot.settings import TARIF_ARBITRARY, TARIF_GROUP, TARIF_IND, TARIF_SECTION, TARIF_FEW, DEBUG


class ModelwithTimeManager(models.Manager):
    def tr_day_is_my_available(self, *args, **kwargs):
        return self.filter(is_available=True, tr_day_status=GroupTrainingDay.MY_TRAIN_STATUS, *args, **kwargs)


class ModelwithTime(models.Model):
    dttm_added = models.DateTimeField(default=timezone.now)
    dttm_deleted = models.DateTimeField(null=True, blank=True)

    objects = ModelwithTimeManager()

    class Meta:
        abstract = True


class User(AbstractUser):
    STATUS_WAITING = 'W'
    STATUS_TRAINING = 'G'
    STATUS_FINISHED = 'F'
    STATUS_ARBITRARY = 'A'
    STATUS_IND_TRAIN = 'I'
    STATUSES = (
        (STATUS_WAITING, 'в ожидании'),
        (STATUS_TRAINING, 'групповые тренировки'),
        (STATUS_ARBITRARY, 'свободный график'),
        (STATUS_FINISHED, 'закончил'),
    )

    tarif_for_status = {
        STATUS_TRAINING: TARIF_GROUP,
        STATUS_ARBITRARY: TARIF_ARBITRARY,
        STATUS_IND_TRAIN: TARIF_IND,
    }

    id = models.BigIntegerField(primary_key=True)  # telegram id
    telegram_username = models.CharField(max_length=64, null=True, blank=True)
    first_name = models.CharField(max_length=32, null=True, verbose_name='Имя')
    phone_number = models.CharField(max_length=16, null=True, verbose_name='Номер телефона')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, verbose_name='Родитель',
                               related_name='children')

    is_superuser = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    status = models.CharField(max_length=1, choices=STATUSES, default=STATUS_WAITING, verbose_name='статус')

    time_before_cancel = models.DurationField(null=True, help_text='ЧАСЫ:МИНУТЫ:СЕКУНДЫ',
                                              verbose_name='Время, за которое нужно предупредить', default=timedelta(hours=6))
    bonus_lesson = models.SmallIntegerField(null=True, blank=True, default=0, verbose_name='Количество отыгрышей')

    add_info = models.CharField(max_length=128, null=True, blank=True, verbose_name='Доп. информация')

    class Meta:
        verbose_name = 'игрок'
        verbose_name_plural = 'игроки'

    def __str__(self):
        return '{} {} -- {}'.format(self.first_name, self.last_name, self.phone_number)

    @classmethod
    def get_user_and_created(cls, update, context):
        """ python-telegram-bot's Update, Context --> User instance """
        data = extract_user_data_from_update(update)
        u, created = cls.objects.update_or_create(
            id=data["id"],
            defaults={
                'telegram_username': data['username'] if data.get('username') else None,
                'username': data['id'],
                'is_blocked': data['is_blocked']
            }
        )

        if created:
            if context is not None and context.args is not None and len(context.args) > 0:
                payload = context.args[0]
                if str(payload).strip() != str(data["id"]).strip():  # you can't invite yourself
                    u.deep_link = payload
                    u.save()

        return u, created


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'parent', 'status', 'time_before_cancel',
                  'bonus_lesson', 'add_info']

    def clean(self):
        if 'status' in self.changed_data:
            new_status = self.cleaned_data.get('status')
            if self.instance.status == User.STATUS_WAITING and (
                    new_status == User.STATUS_ARBITRARY or new_status == User.STATUS_TRAINING):
                text = NOW_YOU_HAVE_ACCESS_CONGRATS
                reply_markup = construct_main_menu(self.instance, self.instance.status)

                clear_broadcast_messages(
                    user_ids=[self.instance.id],
                    message=text,
                    reply_markup=reply_markup
                )


class TrainingGroup(ModelwithTime):
    STATUS_4IND = 'I'
    STATUS_GROUP = 'G'
    STATUS_FEW = 'F'
    STATUS_SECTION = 'S'
    GROUP_STATUSES = (
        (STATUS_4IND, 'для индивидуальных тренировок'),
        (STATUS_GROUP, 'взрослые групповые тренировки'),
        (STATUS_FEW, 'детская группа малой численности'),
        (STATUS_SECTION, 'детская секция'),
    )

    LEVEL_ORANGE = 'O'
    LEVEL_GREEN = 'G'
    GROUP_LEVELS = (
        (LEVEL_GREEN, GREEN_BALL),
        (LEVEL_ORANGE, ORANGE_BALL),
    )

    name = models.CharField(max_length=32, verbose_name='Название')
    users = models.ManyToManyField(User)
    max_players = models.SmallIntegerField(default=6, verbose_name='Максимальное количество игроков в группе')
    status = models.CharField(max_length=1, choices=GROUP_STATUSES, verbose_name='Статус группы', default=STATUS_GROUP)
    level = models.CharField(max_length=1, choices=GROUP_LEVELS, verbose_name='Уровень группы', default=LEVEL_ORANGE)
    tarif_for_one_lesson = models.PositiveIntegerField(default=400, verbose_name='Тариф за одно занятие')
    available_for_additional_lessons = models.BooleanField(default=False, verbose_name='Занятия за деньги',
                                                           help_text='Можно ли прийти в эту группу на занятия за деньги,'
                                                                     'если меньше, чем max_players')
    order = models.PositiveSmallIntegerField(default=0, blank=True)

    class Meta:
        verbose_name = 'банда'
        verbose_name_plural = 'банды'

    def __str__(self):
        return '{}, max_players: {}'.format(self.name, self.max_players)

    def save(self, *args, **kwargs):
        # для того, чтобы БАНДА №10 была позже БАНДА №1
        number_in_name = re.findall(r'\d+', self.name)
        if len(number_in_name) == 1:
            self.order = number_in_name[0]
        super(TrainingGroup, self).save(*args, **kwargs)


class TrainingGroupForm(forms.ModelForm):
    class Meta:
        model = TrainingGroup
        fields = ['name', 'users', 'max_players', 'status', 'level',
                  'tarif_for_one_lesson', 'available_for_additional_lessons']

    def clean(self):
        users = self.cleaned_data.get('users')
        max_players = self.cleaned_data.get('max_players')
        if users.count() > max_players:
            raise ValidationError(
                {'max_players': ERROR_LIMIT_MAX_PLAYERS.format(max_players, users.count())})

        if 'users' in self.changed_data:
            tr_day = GroupTrainingDay.objects.filter(group__max_players__gt=1, group=self.instance, ).annotate(
                                        start=ExpressionWrapper(F('start_time') + F('date'), output_field=DateTimeField()),
                                        group_users_cnt=Count('group__users', distinct=True),
                                        absent_cnt=Count('absent', distinct=True),
                                        visitors_cnt=Count('visitors', distinct=True),
                                        pay_visitors_cnt=Count('visitors', distinct=True),
                                        max_players=F('group__max_players')).filter(
                                                group_users_cnt__lt=users.count(),
                                                start__gte=moscow_datetime(datetime.now()),
                                                is_available=True,
                                                max_players=F('visitors_cnt') +
                                                            F('pay_visitors_cnt') +
                                                            F('group_users_cnt') -
                                                            F('absent_cnt')).distinct().values('id', 'date', 'start_time')
            if len(tr_day):
                error_ids = "\n".join(['<a href="http://vladlen82.fvds.ru/tgadmin/base/grouptrainingday/{}/change/">{} {}</a>'.format(x['id'], x['date'], x['start_time']) for x in tr_day])
                error_text = f"{ERROR_MAX_PLAYERS_IN_FUTURE}:\n{error_ids}"
                raise ValidationError(
                    {'users': mark_safe(error_text)})


class GroupTrainingDay(ModelwithTime):
    MY_TRAIN_STATUS = 'M'
    RENT_TRAIN_STATUS = 'R'

    TR_DAY_STATUSES = (
        (MY_TRAIN_STATUS, 'моя тренировка'),
        (RENT_TRAIN_STATUS, 'аренда')
    )

    group = models.ForeignKey(TrainingGroup, on_delete=models.PROTECT, verbose_name='Группа')
    absent = models.ManyToManyField(User, blank=True, help_text='Кто сегодня отсутствует', verbose_name='Отсутствующие')
    date = models.DateField(default=timezone.now, verbose_name='Дата Занятия')
    is_available = models.BooleanField(default=True, help_text='Будет ли в этот день тренировка у этой группы')
    start_time = models.TimeField(null=True, help_text='ЧАСЫ:МИНУТЫ:СЕКУНДЫ', verbose_name='Время начала занятия')
    duration = models.DurationField(null=True, default=timedelta(hours=1), help_text='ЧАСЫ:МИНУТЫ:СЕКУНДЫ',
                                    verbose_name='Продолжительность занятия')
    visitors = models.ManyToManyField(User, blank=True, help_text='Пришли из других групп\n', related_name='visitors',
                                      verbose_name='Игроки из других групп')

    pay_visitors = models.ManyToManyField(User, blank=True, help_text='Заплатили за занятие',
                                          related_name='pay_visitors', verbose_name='Заплатившие игроки')
    tr_day_status = models.CharField(max_length=1, default=MY_TRAIN_STATUS, help_text='Моя тренировка или аренда',
                                     choices=TR_DAY_STATUSES, verbose_name='Статус')

    is_individual = models.BooleanField(default=False, help_text='индивидуальная ли тренировка')

    class Meta:
        ordering = ['-date']
        verbose_name = 'тренировочный день'
        verbose_name_plural = 'тренировочные дни'

    def __str__(self):
        return 'Группа: {}, дата тренировки {}, время начала: {}'.format(self.group, self.date, self.start_time)


class GroupTrainingDayForm(forms.ModelForm):
    class Meta:
        model = GroupTrainingDay
        fields = ['group', 'absent', 'visitors', 'pay_visitors', 'date', 'is_available', 'is_individual', 'tr_day_status', 'start_time',
                  'duration']

    def clean(self):

        def send_alert_about_cancel_in_visitors(self, type_of_visitors='visitors'):
            canceled_users = None
            if type_of_visitors == 'visitors':
                if self.cleaned_data.get(type_of_visitors).count() < self.instance.visitors.count():
                    canceled_users = self.instance.visitors.all().exclude(
                        id__in=self.cleaned_data.get(type_of_visitors))
            elif type_of_visitors == 'pay_visitors':
                if self.cleaned_data.get(type_of_visitors).count() < self.instance.pay_visitors.count():
                    canceled_users = self.instance.pay_visitors.all().exclude(
                        id__in=self.cleaned_data.get(type_of_visitors))

            if canceled_users:
                text = CANCEL_TRAIN_PLUS_BONUS_LESSON.format(self.cleaned_data.get("date"))

                clear_broadcast_messages(
                    list(canceled_users.values_list('id', flat=True)),
                    text,
                    reply_markup=construct_main_menu()
                )

                canceled_users.update(bonus_lesson=F('bonus_lesson') + 1)

        group = self.cleaned_data.get('group')

        if not group:
            raise ValidationError('Не выбрана группа')

        current_amount_of_players = self.cleaned_data.get('visitors').count() + \
                                        self.cleaned_data.get('pay_visitors').count() + \
                                            group.users.count() - self.cleaned_data.get('absent').count()
        if current_amount_of_players > group.max_players:
            raise ValidationError(ERROR_LIMIT_MAX_PLAYERS.format(group.max_players, current_amount_of_players))
        if 'start_time' in self.changed_data or 'duration' in self.changed_data or 'date' in self.changed_data:
            """
                Если добавляется новый grouptrainingday, то нужно
                проверить, не накладывается ли время тренировки
                на уже существущие.
            """
            exist_trainings = GroupTrainingDay.objects.filter(date=self.cleaned_data.get('date'))
            start_time = datetime.combine(self.cleaned_data.get('date'), self.cleaned_data.get('start_time'))

            for train in exist_trainings:
                exist_train_start_time = datetime.combine(train.date, train.start_time)
                if exist_train_start_time <= start_time < exist_train_start_time + train.duration:
                    raise ValidationError(ERROR_CANT_ADD_NEW_TRAIN.format(train.start_time, train.duration))

            # send alert to players about changing lesson parameters
            # check only existing tr_days
            if GroupTrainingDay.objects.filter(group=self.cleaned_data.get('group'), date=self.cleaned_data.get('date'),
                                               start_time=self.cleaned_data.get('start_time'),
                                               duration=self.cleaned_data.get('duration'),
                                               ).count():
                changed_data_custom = []
                before_after_text = ''
                if 'start_time' in self.changed_data:
                    changed_data_custom.append('время начала тренировки')
                    before_after_text += self.instance.start_time.strftime(TM_TIME_SCHEDULE_FORMAT)
                    before_after_text += f" 🔜 {self.cleaned_data.get('start_time').strftime(TM_TIME_SCHEDULE_FORMAT)}\n"
                if 'duration' in self.changed_data:
                    changed_data_custom.append('продолжительность занятия')
                    before_after_text += str(self.instance.duration)
                    before_after_text += f" 🔜 {self.cleaned_data.get('duration')}\n"
                if 'date' in self.changed_data:
                    changed_data_custom.append('дата проведения занятия')
                    before_after_text += self.instance.date.strftime(DT_BOT_FORMAT)
                    before_after_text += f" 🔜 {self.cleaned_data.get('date').strftime(DT_BOT_FORMAT)}"

                day_of_week = from_eng_to_rus_day_week[calendar.day_name[self.instance.date.weekday()]]
                text = f'⚠️ATTENTION⚠️\n' \
                       f'Изменились следующие параметры тренировки {self.instance.date.strftime(DT_BOT_FORMAT)}' \
                       f' ({day_of_week}): {", ".join(changed_data_custom)}\n' \
                       f'{before_after_text}'
                send_alert_about_changing_tr_day_time(self.instance, text)

        if 'is_available' in self.changed_data:  # если статут дня меняется, то отсылаем алерт об изменении
            send_alert_about_changing_tr_day_status(self.instance, self.cleaned_data.get('is_available'))

        if 'visitors' in self.changed_data:
            send_alert_about_cancel_in_visitors(self, 'visitors')

        if 'pay_visitors' in self.changed_data:
            send_alert_about_cancel_in_visitors(self, 'pay_visitors')


class Payment(models.Model):
    JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER = '1', '2', '3', '4', '5', '6', '7', '8', '9'
    OCTOBER, NOVEMBER, DECEMBER = '10', '11', '12'

    MONTHS = (
        (JANUARY, 'январь'), (FEBRUARY, 'февраль'), (MARCH, 'март'), (APRIL, 'апрель'), (MAY, 'май'),
        (JUNE, 'июнь'), (JULY, 'июль'), (AUGUST, 'август'), (SEPTEMBER, 'сентябрь'), (OCTOBER, 'октябрь'),
        (NOVEMBER, 'ноябрь'), (DECEMBER, 'декабрь')
    )

    YEAR_2020 = '0'
    YEAR_2021 = '1'

    YEARS = (
        (YEAR_2020, '2020'), (YEAR_2021, '2021')
    )

    player = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='игрок', null=True)
    month = models.CharField(max_length=2, choices=MONTHS, verbose_name='месяц')
    year = models.CharField(max_length=1, choices=YEARS, verbose_name='год')
    fact_amount = models.PositiveIntegerField(verbose_name='Сколько заплатил', null=True, default=0)
    theory_amount = models.PositiveIntegerField(verbose_name='Сколько должен был заплатить', null=True, default=0)
    n_fact_visiting = models.PositiveSmallIntegerField(verbose_name='Кол-во посещенных занятий', null=True, default=0)

    class Meta:
        ordering = ['year']
        verbose_name = 'оплата'
        verbose_name_plural = 'оплата'

    def save(self, *args, **kwargs):
        year = int(self.year) + 2020
        month = int(self.month)
        begin_day_month = date(year, month, 1)

        base_query = GroupTrainingDay.objects.filter(Q(visitors__in=[self.player]) | Q(group__users__in=[self.player]),
                                                     date__gte=begin_day_month,
                                                     date__lte=moscow_datetime(datetime.now()).date(),
                                                     is_available=True,
                                                     date__month=month).exclude(absent__in=[self.player])

        self.n_fact_visiting = base_query.distinct().count()

        payment = 0
        for x in self.player.traininggroup_set.all().iterator():
            if x.status == TrainingGroup.STATUS_SECTION:
                payment = TARIF_SECTION
        if not payment:
            payment = base_query.annotate(
                gr_status=F('group__status')).annotate(
                tarif=Case(When(gr_status=TrainingGroup.STATUS_4IND, then=TARIF_IND),
                           When(gr_status=TrainingGroup.STATUS_GROUP, then=TARIF_GROUP),
                           When(gr_status=TrainingGroup.STATUS_FEW, then=TARIF_FEW),
                           output_field=IntegerField())).distinct().aggregate(
                sigma=Sum('tarif'))['sigma']

        self.theory_amount = payment

        super(Payment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.player}, месяц: {self.month}"


class AlertsLog(models.Model):
    COMING_TRAIN = 'CT'
    CUSTOM_COACH_MESSAGE = 'CM'
    SHOULD_PAY = 'SP'

    ALERT_TYPES = (
        (COMING_TRAIN, 'предстоящая тренировка'),
        (CUSTOM_COACH_MESSAGE, 'сообщение от тренера'),
        (SHOULD_PAY, 'нужно заплатить за месяц')
    )

    player = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_sent = models.BooleanField(default=False)
    dttm_sent = models.DateTimeField(auto_now_add=True)
    tr_day = models.ForeignKey(GroupTrainingDay, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    alert_type = models.CharField(max_length=2, choices=ALERT_TYPES, default=COMING_TRAIN)
    info = models.TextField(null=True)

    def __str__(self):
        return f"{self.player, self.tr_day}"


"""раздел с сигналами, в отедльном файле что-то не пошло"""


@receiver(post_save, sender=GroupTrainingDay)
def create_training_days_for_next_two_months(sender, instance, created, **kwargs):
    """
    При создании instance GroupTrainingDay автоматом добавляем
    еще таких же записей примерно на 2 месяца вперед.
    Используем bulk_create, т.к. иначе получим рекурсию.
    """
    pass
    # if created:
    #     period = 8 if instance.group.status == TrainingGroup.STATUS_4IND else 24
    #     date = instance.date + timedelta(days=7)
    #     dates = [date]
    #     for _ in range(period):
    #         date += timedelta(days=7)
    #         dates.append(date)
    #     objs = [GroupTrainingDay(group=instance.group, date=dat, start_time=instance.start_time,
    #                              duration=instance.duration) for dat in dates]
    #     GroupTrainingDay.objects.bulk_create(objs)


@receiver(post_delete, sender=GroupTrainingDay)
def delete_training_days(sender, instance, **kwargs):
    """
        При удалении instance GroupTrainingDay автоматом удаляем
        занятие в это время для более поздних дат.
    """
    GroupTrainingDay.objects.filter(group=instance.group, start_time=instance.start_time, duration=instance.duration,
                                    date__gt=instance.date).delete()


@receiver(post_save, sender=User)
def create_group_for_arbitrary(sender, instance, created, **kwargs):
    """
        Если игрок ходит по свободному графику, то создадим
        для него группу, состояющую только из него.
    """
    if instance.status == User.STATUS_ARBITRARY:
        group, _ = TrainingGroup.objects.get_or_create(
            name=instance.first_name + instance.last_name,
            max_players=1,
            status=TrainingGroup.STATUS_4IND
        )
        if not group.users.count():
            group.users.add(instance)

import re

import telegram
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Q, F, Case, When, Sum, IntegerField
from django.utils import timezone
from datetime import datetime, date, timedelta

from base.utils import moscow_datetime, extract_user_data_from_update
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from tele_interface.static_text import *
from tennis_bot.settings import TARIF_ARBITRARY, TARIF_GROUP, TARIF_IND, TARIF_SECTION, TARIF_FEW, TELEGRAM_TOKEN, DEBUG


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

    def save(self, *args, **kwargs):
        if not self.username and DEBUG:
            self.username = self.id
        super(User, self).save()


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

    @classmethod
    def get_or_create_ind_group_for_user(cls, user: User):
        group, _ = cls.objects.create(
            name=user.first_name + user.last_name, status=TrainingGroup.STATUS_4IND, max_players=1
        )
        return group

    def save(self, *args, **kwargs):
        # для того, чтобы БАНДА №10 была позже БАНДА №1
        number_in_name = re.findall(r'\d+', self.name)
        if len(number_in_name) == 1:
            self.order = number_in_name[0]
        super(TrainingGroup, self).save(*args, **kwargs)


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
    pay_bonus_visitors = models.ManyToManyField(User, blank=True, help_text='Платный отыгрыш',
                                                related_name='pay_bonus_visitors', verbose_name='Заплатили ₽ + отыгрыш')

    tr_day_status = models.CharField(max_length=1, default=MY_TRAIN_STATUS, help_text='Моя тренировка или аренда',
                                     choices=TR_DAY_STATUSES, verbose_name='Статус')
    is_individual = models.BooleanField(default=False, help_text='индивидуальная ли тренировка')

    class Meta:
        ordering = ['-date']
        verbose_name = 'тренировочный день'
        verbose_name_plural = 'тренировочные дни'

    def __str__(self):
        return 'Группа: {}, дата тренировки {}, время начала: {}'.format(self.group, self.date, self.start_time)


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


class Photo(models.Model):
    url = models.TextField(null=True, blank=True, verbose_name='Ссылка на картинку')
    telegram_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='id картинки на сервере телеграма')
    text = models.TextField(null=True, blank=True, verbose_name='Текстовое описание')

    class Meta:
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'

    def check_if_telegram_id_is_present(self):
        return True if self.telegram_id else False

    def save_telegram_id(self, tg_token=TELEGRAM_TOKEN):
        bot = telegram.Bot(tg_token)
        photo_message = bot.send_photo(
            350490234,
            photo=self.url,
            disable_notification=True
        ).to_dict()
        self.telegram_id = photo_message['photo'][-1]['file_id']
        self.save()


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

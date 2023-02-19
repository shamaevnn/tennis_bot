from __future__ import annotations

import logging
import random
import re
from typing import Optional, Tuple, Union, Iterator
from uuid import uuid4

import telegram
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import (
    Q,
    F,
    Case,
    When,
    Sum,
    IntegerField,
    QuerySet,
)
from django.utils import timezone
from datetime import datetime, date, timedelta

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from telegram import Update, Bot, ParseMode
from telegram.ext import CallbackContext

from base.utils.db_managers import GetOrNoneManager, CoachPlayerManager
from base.utils.models import ModelwithTime, nb
from base.utils.telegram import extract_user_data_from_update
from tennis_bot.settings import (
    TARIF_ARBITRARY,
    TARIF_GROUP,
    TARIF_IND,
    TARIF_SECTION,
    TARIF_FEW,
    TELEGRAM_TOKEN,
    ADMIN_CHAT_ID,
    HOST,
)


class User(AbstractUser):
    """используется для логина в админку"""

    id = models.AutoField(
        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
    )
    first_name = models.CharField(max_length=32, **nb, verbose_name="Имя")

    def __str__(self):
        return self.get_full_name()


class Player(models.Model):
    STATUS_WAITING = "W"
    STATUS_TRAINING = "G"
    STATUS_FINISHED = "F"
    STATUS_ARBITRARY = "A"
    STATUS_IND_TRAIN = "I"
    STATUSES = (
        (STATUS_WAITING, "в ожидании"),
        (STATUS_TRAINING, "групповые тренировки"),
        (STATUS_ARBITRARY, "свободный график"),
        (STATUS_FINISHED, "закончил"),
    )

    id = models.UUIDField(primary_key=True, unique=True, default=uuid4)

    first_name = models.CharField(max_length=32, null=True, verbose_name="Имя")
    last_name = models.CharField(max_length=32, null=True, verbose_name="Фамилия")
    phone_number = models.CharField(
        max_length=16, null=True, verbose_name="Номер телефона"
    )
    parent = models.ForeignKey(
        "self",
        on_delete=models.PROTECT,
        verbose_name="Родитель",
        related_name="children",
        **nb,
    )

    tg_id = models.PositiveBigIntegerField(verbose_name="telegram id", **nb)
    tg_username = models.CharField(max_length=64, **nb)
    has_blocked_bot = models.BooleanField(
        default=False, verbose_name="заблокировал бота"
    )
    deep_link = models.CharField(max_length=64, **nb)

    status = models.CharField(
        max_length=1, choices=STATUSES, default=STATUS_WAITING, verbose_name="статус"
    )
    time_before_cancel = models.DurationField(
        null=True,
        help_text="ЧАСЫ:МИНУТЫ:СЕКУНДЫ",
        verbose_name="Время, за которое нужно предупредить",
        default=timedelta(hours=6),
    )
    bonus_lesson = models.SmallIntegerField(
        default=0, verbose_name="Количество отыгрышей"
    )
    max_lessons_for_bonus_in_future = models.PositiveSmallIntegerField(
        default=3, verbose_name="Ограничение на кол-во тренировок за отыгрыши"
    )
    is_coach = models.BooleanField(default=False, verbose_name="Тренер ли")

    objects = GetOrNoneManager()
    coaches = CoachPlayerManager()

    class Meta:
        verbose_name = "игрок"
        verbose_name_plural = "игроки"

    def __str__(self):
        return "{} {} -- {}".format(self.first_name, self.last_name, self.phone_number)

    @property
    def tg_name(self) -> str:
        return f"@{self.tg_username}" if self.tg_username else f"{self.tg_id}"

    @property
    def get_link_to_django_admin(self) -> str:
        return f"{HOST}player/{self.id}/change/"

    def count_not_self_group_trainings_in_future(self):
        """
        Считаем на сколько тренировок записался игрок в будущем в другую группу,
        либо за отыгрыши, либо за платные отыгрыши
        """
        return GroupTrainingDay.objects.filter(
            Q(visitors__in=[self])
            | Q(pay_visitors__in=[self])
            | Q(pay_bonus_visitors__in=[self]),
            date__gte=datetime.now(),
        ).count()

    @classmethod
    def from_update(cls, update: Update) -> Optional[Player]:
        data = extract_user_data_from_update(update)
        tg_id = data["id"]
        player = cls.objects.get_or_none(tg_id=tg_id)
        return player

    @classmethod
    def get_player_and_created(
        cls, update: Update, context: CallbackContext
    ) -> Tuple[Player, bool]:
        """python-telegram-bot's Update, Context --> User instance"""
        data = extract_user_data_from_update(update)
        tg_id = data["id"]
        u, created = cls.objects.update_or_create(
            tg_id=tg_id,
            defaults={
                "tg_username": data["username"] if data.get("username") else None,
                "has_blocked_bot": data["is_blocked"],
            },
        )

        if created:
            if (
                context is not None
                and context.args is not None
                and len(context.args) > 0
            ):
                payload = context.args[0]
                if (
                    str(payload).strip() != str(tg_id).strip()
                ):  # you can't invite yourself
                    u.deep_link = payload
                    u.save()
        return u, created

    @classmethod
    def get_tarif_by_status(cls, status: str) -> int:
        tarif_by_status = {
            cls.STATUS_TRAINING: TARIF_GROUP,
            cls.STATUS_ARBITRARY: TARIF_ARBITRARY,
            cls.STATUS_IND_TRAIN: TARIF_IND,
        }
        return tarif_by_status[status]


class TrainingGroup(ModelwithTime):
    STATUS_RENT = "R"
    STATUS_4IND = "I"
    STATUS_GROUP = "G"
    STATUS_FEW = "F"
    STATUS_SECTION = "S"
    GROUP_STATUSES = (
        (STATUS_4IND, "для индивидуальных тренировок"),
        (STATUS_RENT, "для аренды корта"),
        (STATUS_GROUP, "взрослые групповые тренировки"),
        (STATUS_FEW, "детская группа малой численности"),
        (STATUS_SECTION, "детская секция"),
    )

    LEVEL_ORANGE = "O"
    LEVEL_GREEN = "G"
    GROUP_LEVEL_DICT = {LEVEL_ORANGE: "🟠оранжевый мяч🟠", LEVEL_GREEN: "🟢зелёный мяч🟢"}
    GROUP_LEVELS = (
        (LEVEL_GREEN, GROUP_LEVEL_DICT[LEVEL_GREEN]),
        (LEVEL_ORANGE, GROUP_LEVEL_DICT[LEVEL_ORANGE]),
    )

    name = models.CharField(max_length=32, verbose_name="Название")
    players = models.ManyToManyField(Player, verbose_name="Игроки группы")
    max_players = models.SmallIntegerField(default=6, verbose_name="Макс. игроков")
    status = models.CharField(
        max_length=1,
        choices=GROUP_STATUSES,
        verbose_name="Статус группы",
        default=STATUS_GROUP,
    )
    level = models.CharField(
        max_length=1,
        choices=GROUP_LEVELS,
        verbose_name="Уровень группы",
        default=LEVEL_ORANGE,
    )
    tarif_for_one_lesson = models.PositiveIntegerField(
        default=400, verbose_name="Тариф за одно занятие"
    )
    available_for_additional_lessons = models.BooleanField(
        default=False,
        verbose_name="Занятия за деньги",
        help_text="Можно ли прийти в эту группу на занятия за деньги, если меньше, чем max_players",
    )
    order = models.PositiveSmallIntegerField(default=0, blank=True)

    class Meta:
        verbose_name = "банда"
        verbose_name_plural = "банды"

    def __str__(self):
        return "{}, max_players: {}".format(self.name, self.max_players)

    @classmethod
    def get_banda_groups(cls) -> QuerySet[TrainingGroup]:
        banda_groups = TrainingGroup.objects.filter(
            status=TrainingGroup.STATUS_GROUP,
            max_players__gt=1,
            name__iregex=r"БАНДА",
        ).order_by("order")
        return banda_groups

    @classmethod
    def _get_or_create_ind_or_rent_group(
        cls, player: Player, status: str
    ) -> TrainingGroup:
        assert status in (cls.STATUS_RENT, cls.STATUS_4IND)
        group, _ = cls.objects.get_or_create(
            name=f"{player.first_name}{player.last_name}", status=status, max_players=1
        )
        if player not in group.players.all():
            group.players.add(player)
        return group

    @classmethod
    def get_or_create_ind_group(cls, player: Player) -> TrainingGroup:
        return cls._get_or_create_ind_or_rent_group(player, status=cls.STATUS_4IND)

    @classmethod
    def get_or_create_rent_group(cls, player: Player) -> TrainingGroup:
        return cls._get_or_create_ind_or_rent_group(player, status=cls.STATUS_RENT)

    def save(self, *args, **kwargs):
        # для того, чтобы БАНДА №10 была позже БАНДА №1
        number_in_name = re.findall(r"\d+", self.name)
        if len(number_in_name) == 1:
            self.order = number_in_name[0]
        super(TrainingGroup, self).save(*args, **kwargs)


class GroupTrainingDay(ModelwithTime):
    GROUP_ADULT_TRAIN = "M"
    INDIVIDUAL_TRAIN = "I"
    RENT_COURT_STATUS = "R"

    TR_DAY_STATUSES = (
        (GROUP_ADULT_TRAIN, "групповая тренировка для взрослых"),
        (INDIVIDUAL_TRAIN, "индивидуальная тренировка"),
        (RENT_COURT_STATUS, "аренда корта"),
    )

    group = models.ForeignKey(
        TrainingGroup, on_delete=models.PROTECT, verbose_name="Группа"
    )
    date = models.DateField(default=timezone.now, verbose_name="Дата Занятия")
    is_available = models.BooleanField(
        default=True,
        help_text="Будет ли в этот день тренировка у этой группы",
        verbose_name="Доступно",
    )
    start_time = models.TimeField(
        null=True, help_text="ЧАСЫ:МИНУТЫ:СЕКУНДЫ", verbose_name="Время начала занятия"
    )
    duration = models.DurationField(
        null=True,
        default=timedelta(hours=1),
        help_text="ЧАСЫ:МИНУТЫ:СЕКУНДЫ",
        verbose_name="Продолжительность занятия",
    )

    absent = models.ManyToManyField(
        Player,
        blank=True,
        help_text="Кто сегодня отсутствует",
        verbose_name="Отсутствующие",
    )

    visitors = models.ManyToManyField(
        Player,
        blank=True,
        help_text="Пришли из других групп\n",
        related_name="visitors",
        verbose_name="Игроки из других групп",
    )

    pay_visitors = models.ManyToManyField(
        Player,
        blank=True,
        help_text="Заплатили за занятие",
        related_name="pay_visitors",
        verbose_name="Заплатившие игроки",
    )

    pay_bonus_visitors = models.ManyToManyField(
        Player,
        blank=True,
        help_text="Платный отыгрыш",
        related_name="pay_bonus_visitors",
        verbose_name="Заплатили ₽ + отыгрыш",
    )

    status = models.CharField(
        max_length=1,
        default=GROUP_ADULT_TRAIN,
        help_text="Моя тренировка или аренда",
        choices=TR_DAY_STATUSES,
        verbose_name="Статус",
    )
    is_deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date"]
        verbose_name = "тренировочный день"
        verbose_name_plural = "тренировочные дни"

    def __str__(self):
        return "Группа: {}, дата {}, начало в: {}".format(
            self.group, self.date, self.start_time
        )

    @property
    def start_dttm(self):
        return datetime.combine(self.date, self.start_time)

    @classmethod
    def get_tr_days_for_alerting_about_coming_train(cls) -> Iterator[GroupTrainingDay]:
        HOURS_BETWEEN_NOW_AND_COMING_TRAINING = 5
        now = datetime.now()
        available_tr_days: QuerySet[GroupTrainingDay] = (
            cls.objects.select_related("group")
            .prefetch_related(
                "absent", "visitors", "pay_visitors", "pay_bonus_visitors"
            )
            .filter(is_available=True)
        )
        for tr_day in available_tr_days.iterator():
            if tr_day.start_dttm > now and tr_day.start_dttm - now < timedelta(
                hours=HOURS_BETWEEN_NOW_AND_COMING_TRAINING
            ):
                yield tr_day

    def create_tr_days_for_future(self):
        NUMBER_OF_WEEKS_IN_2_MONTHS = 8
        NUMBER_OF_WEEKS_IN_SEASON = 26  # 6 месяцев

        period = (
            NUMBER_OF_WEEKS_IN_2_MONTHS
            if self.group.status
            in (TrainingGroup.STATUS_4IND, TrainingGroup.STATUS_RENT)
            else NUMBER_OF_WEEKS_IN_SEASON
        )
        init_date = self.date + timedelta(days=7)
        instances = []
        for _ in range(period):
            instances.append(
                GroupTrainingDay(
                    group=self.group,
                    date=init_date,
                    start_time=self.start_time,
                    duration=self.duration,
                    status=self.status,
                )
            )
            init_date += timedelta(days=7)

        print(instances)
        GroupTrainingDay.objects.bulk_create(instances)


class Payment(models.Model):
    JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER = (
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
    )
    OCTOBER, NOVEMBER, DECEMBER = "10", "11", "12"

    MONTHS = (
        (JANUARY, "январь"),
        (FEBRUARY, "февраль"),
        (MARCH, "март"),
        (APRIL, "апрель"),
        (MAY, "май"),
        (JUNE, "июнь"),
        (JULY, "июль"),
        (AUGUST, "август"),
        (SEPTEMBER, "сентябрь"),
        (OCTOBER, "октябрь"),
        (NOVEMBER, "ноябрь"),
        (DECEMBER, "декабрь"),
    )

    YEAR_2020 = "0"
    YEAR_2021 = "1"
    YEAR_2022 = "2"
    YEAR_2023 = "3"

    YEARS = ((YEAR_2020, "2020"), (YEAR_2021, "2021"), (YEAR_2022, "2022"), (YEAR_2023, "2023"))

    player = models.ForeignKey(
        Player, on_delete=models.SET_NULL, verbose_name="игрок", null=True
    )
    month = models.CharField(max_length=2, choices=MONTHS, verbose_name="месяц")
    year = models.CharField(max_length=1, choices=YEARS, verbose_name="год")
    fact_amount = models.PositiveIntegerField(
        verbose_name="Сколько заплатил", null=True, default=0
    )
    theory_amount = models.PositiveIntegerField(
        verbose_name="Сколько должен был заплатить", null=True, default=0
    )
    n_fact_visiting = models.PositiveSmallIntegerField(
        verbose_name="Кол-во посещенных занятий", null=True, default=0
    )

    class Meta:
        ordering = ["year"]
        verbose_name = "оплата"
        verbose_name_plural = "оплата"

    def save(self, *args, **kwargs):
        """
        Подсчитваем сколько теоритечески в данный месяц должен заплатить игрок.
        Учитываем посещения и пропуски
        """
        year = int(self.year) + 2020
        month = int(self.month)
        begin_day_month = date(year, month, 1)

        # тренировки игрока в текущем месяце
        # те, которые пропустил, не считаются
        base_query = GroupTrainingDay.objects.filter(
            Q(visitors__in=[self.player]) | Q(group__players__in=[self.player]),
            date__gte=begin_day_month,
            date__lte=datetime.now().date(),
            is_available=True,
            date__month=month,
        ).exclude(absent__in=[self.player])

        player_in_section = False
        for x in self.player.traininggroup_set.all().iterator():
            if x.status == TrainingGroup.STATUS_SECTION:
                player_in_section = True

        # если занимается в секции, то фиксированная сумма за месяц
        # иначе сумируем стоимость каждого занятия
        if player_in_section:
            payment_sum = TARIF_SECTION
        else:
            payment_sum = (
                base_query.annotate(gr_status=F("group__status"))
                .annotate(
                    tarif=Case(
                        When(gr_status=TrainingGroup.STATUS_4IND, then=TARIF_IND),
                        When(gr_status=TrainingGroup.STATUS_GROUP, then=TARIF_GROUP),
                        When(gr_status=TrainingGroup.STATUS_FEW, then=TARIF_FEW),
                        output_field=IntegerField(),
                    )
                )
                .distinct()
                .aggregate(sigma=Sum("tarif"))["sigma"]
            )

        self.n_fact_visiting = base_query.distinct().count()
        self.theory_amount = payment_sum
        super(Payment, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.player}, месяц: {self.month}"


class AlertsLog(models.Model):
    COMING_TRAIN = "CT"
    CUSTOM_COACH_MESSAGE = "CM"
    SHOULD_PAY = "SP"

    ALERT_TYPES = (
        (COMING_TRAIN, "предстоящая тренировка"),
        (CUSTOM_COACH_MESSAGE, "сообщение от тренера"),
        (SHOULD_PAY, "нужно заплатить за месяц"),
    )

    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    is_sent = models.BooleanField(default=False)
    dttm_sent = models.DateTimeField(auto_now_add=True)
    tr_day = models.ForeignKey(GroupTrainingDay, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, null=True)
    alert_type = models.CharField(
        max_length=2, choices=ALERT_TYPES, default=COMING_TRAIN
    )
    info = models.TextField(null=True)

    def __str__(self):
        return f"{self.player, self.tr_day}"


class Photo(models.Model):
    url = models.TextField(verbose_name="Ссылка на картинку", **nb)
    telegram_id = models.CharField(
        max_length=256, verbose_name="id картинки на сервере телеграма", **nb
    )
    text = models.TextField(verbose_name="Текстовое описание", **nb)

    class Meta:
        verbose_name = "фотография"
        verbose_name_plural = "фотографии"

    @staticmethod
    def get_random_photo(photos: QuerySet[Photo]) -> Photo:
        return random.choice(photos)

    def send_to_player(self, chat_id: Union[int, str], text: str, bot: Bot) -> bool:
        success = True
        try:
            bot.send_photo(
                chat_id=chat_id,
                photo=self.telegram_id,
                caption=text,
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:
            success = False
            logging.error(
                f"Error while sending photo {self.telegram_id} to {chat_id}:\n{e}"
            )
        return success

    def save(self, **kwargs):
        if not self.telegram_id:
            bot = telegram.Bot(TELEGRAM_TOKEN)
            photo_message = bot.send_photo(
                ADMIN_CHAT_ID, photo=self.url, disable_notification=True
            ).to_dict()
            self.telegram_id = photo_message["photo"][-1]["file_id"]
        super().save(**kwargs)


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
def delete_training_days(sender, instance: GroupTrainingDay, **kwargs):
    """
    При удалении instance GroupTrainingDay автоматом удаляем
    занятие в это время для более поздних дат.
    """
    GroupTrainingDay.objects.filter(
        group=instance.group,
        start_time=instance.start_time,
        duration=instance.duration,
        date__gt=instance.date,
    ).delete()


@receiver(post_save, sender=Player)
def create_group_for_arbitrary(sender, instance: Player, created, **kwargs):
    """
    Если игрок ходит по свободному графику, то создадим
    для него группу, состояющую только из него.
    """
    if instance.status == Player.STATUS_ARBITRARY:
        TrainingGroup.get_or_create_ind_group(instance)

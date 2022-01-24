from django.test import TestCase

from base.models import GroupTrainingDay
from base.utils.for_tests import CreateData


class TestCreateTrDaysForFutureCases(TestCase):
    def setUp(self) -> None:
        self.me = CreateData.group_player(tg_id=1, first_name="Nikita")
        self.individual_group = CreateData.ind_group(player=self.me)
        self.tr_day = CreateData.tr_day_for_group(group=self.individual_group)

    def test_create_tr_days_for_future(self):
        # изначально всего 1 тренировка
        self.assertEqual(1, GroupTrainingDay.objects.all().count())

        # создаем в будущем тренировки
        self.tr_day.create_tr_days_for_future()

        # проверяем, что теперь их 9
        self.assertEqual(9, GroupTrainingDay.objects.all().count())

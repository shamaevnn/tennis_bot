from datetime import datetime, timedelta, time

from django.test import TestCase
from base.models import Player, TrainingGroup
from base.utils.for_tests import CreateData
from player_bot.take_lesson.utils import (
    get_available_start_times_for_given_duration_and_date,
)

_today = datetime.today()
_date = (_today + timedelta(days=2)).date()


class TestAllAvailablePeriods(TestCase):
    @classmethod
    def setUpTestData(self):
        self.player = Player.objects.create(
            tg_id=1, first_name="Nikita", status=Player.STATUS_TRAINING
        )
        self.group = TrainingGroup.objects.create(
            name="Nikita_group", max_players=1, status=TrainingGroup.STATUS_4IND
        )

        self.tr_day_9__10 = CreateData.tr_day_for_group(
            group=self.group, start_time=time(9, 0), duration=timedelta(hours=1)
        )
        self.tr_day_1130__13 = CreateData.tr_day_for_group(
            self.group, start_time=time(11, 30), duration=timedelta(hours=1, minutes=30)
        )
        self.tr_day_1330__1530 = CreateData.tr_day_for_group(
            self.group, start_time=time(13, 30), duration=timedelta(hours=2)
        )
        self.tr_day_1630__1730 = CreateData.tr_day_for_group(
            self.group, start_time=time(16, 30), duration=timedelta(hours=1)
        )
        self.tr_day_1930__21 = CreateData.tr_day_for_group(
            self.group, start_time=time(19, 30), duration=timedelta(hours=1, minutes=30)
        )

    def test_one_hour_period(self):
        start_times = list(
            get_available_start_times_for_given_duration_and_date(
                duration_in_hours="1.0", tr_day_date=_date
            )
        )

        self.assertIn(time(8, 0), start_times)
        self.assertIn(time(10, 0), start_times)
        self.assertIn(time(10, 30), start_times)
        self.assertIn(time(15, 30), start_times)
        self.assertIn(time(17, 30), start_times)
        self.assertIn(time(18, 0), start_times)
        self.assertIn(time(18, 30), start_times)

        self.assertEqual(7, len(start_times))

    def test_one_and_half_hour_period(self):
        start_times = list(
            get_available_start_times_for_given_duration_and_date(
                duration_in_hours="1.5", tr_day_date=_date
            )
        )

        self.assertIn(time(10, 0), start_times)
        self.assertIn(time(17, 30), start_times)
        self.assertIn(time(18, 0), start_times)

        self.assertEqual(3, len(start_times))

    def test_two_hours_period(self):
        start_times = list(
            get_available_start_times_for_given_duration_and_date(
                duration_in_hours="2.0", tr_day_date=_date
            )
        )

        self.assertIn(time(17, 30), start_times)
        self.assertEqual(1, len(start_times))


class TestOnlyOneHour(TestCase):
    @classmethod
    def setUpTestData(self):
        self.player = Player.objects.create(
            tg_id=1, first_name="Nikita", status=Player.STATUS_TRAINING
        )
        self.group = TrainingGroup.objects.create(
            name="Nikita_group", max_players=1, status=TrainingGroup.STATUS_4IND
        )

        self.tr_day_8__10 = CreateData.tr_day_for_group(
            self.group, start_time=time(8, 0), duration=timedelta(hours=2)
        )
        self.tr_day_10__12 = CreateData.tr_day_for_group(
            self.group, start_time=time(10, 0), duration=timedelta(hours=2)
        )
        self.tr_day_1230__14 = CreateData.tr_day_for_group(
            self.group, start_time=time(12, 30), duration=timedelta(hours=1, minutes=30)
        )
        self.tr_day_15__17 = CreateData.tr_day_for_group(
            self.group, start_time=time(15, 0), duration=timedelta(hours=2)
        )
        self.tr_day_18__20 = CreateData.tr_day_for_group(
            self.group, start_time=time(18, 0), duration=timedelta(hours=2)
        )

    def test_one_hour_period(self):
        start_times = list(
            get_available_start_times_for_given_duration_and_date(
                duration_in_hours="1.0", tr_day_date=_date
            )
        )

        self.assertIn(time(14, 0), start_times)
        self.assertIn(time(17, 0), start_times)
        self.assertIn(time(20, 0), start_times)

        self.assertEqual(3, len(start_times))

    def test_one_and_half_hour_period(self):
        start_times = list(
            get_available_start_times_for_given_duration_and_date(
                duration_in_hours="1.5", tr_day_date=_date
            )
        )
        self.assertEqual(0, len(start_times))

    def test_two_hours_period(self):
        start_times = list(
            get_available_start_times_for_given_duration_and_date(
                duration_in_hours="2.0", tr_day_date=_date
            )
        )
        self.assertEqual(0, len(start_times))

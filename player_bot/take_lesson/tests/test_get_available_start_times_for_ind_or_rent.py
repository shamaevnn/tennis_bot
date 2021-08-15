from datetime import datetime, timedelta, time

from django.test import TestCase
from base.models import User, TrainingGroup, GroupTrainingDay
from player_bot.take_lesson.utils import get_available_start_times_for_given_duration_and_date

today = datetime.today()
date = (today + timedelta(days=2)).date()


def create_tr_day_for_group(group, start_time: time, duration: timedelta, **kwargs):
    tr_day = GroupTrainingDay.objects.create(
        group=group, date=date, start_time=start_time, duration=duration, **kwargs
    )
    return tr_day


class TestAllAvailablePeriods(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(
            id=1, username='Nikita', first_name='Nikita', status=User.STATUS_TRAINING, password='123'
        )
        self.group = TrainingGroup.objects.create(name='Nikita_group', max_players=1, status=TrainingGroup.STATUS_4IND)

        self.tr_day_9__10 = create_tr_day_for_group(
            group=self.group, start_time=time(9, 0), duration=timedelta(hours=1)
        )
        self.tr_day_1130__13 = create_tr_day_for_group(self.group, time(11, 30), timedelta(hours=1, minutes=30))
        self.tr_day_1330__1530 = create_tr_day_for_group(self.group, time(13, 30), timedelta(hours=2))
        self.tr_day_1630__1730 = create_tr_day_for_group(self.group, time(16, 30), timedelta(hours=1))
        self.tr_day_1930__21 = create_tr_day_for_group(self.group, time(19, 30), timedelta(hours=1, minutes=30))

    def test_one_hour_period(self):
        start_times = get_available_start_times_for_given_duration_and_date(duration_in_hours='1.0', tr_day_date=date)

        self.assertIn(time(8, 0), start_times)
        self.assertIn(time(10, 0), start_times)
        self.assertIn(time(10, 30), start_times)
        self.assertIn(time(15, 30), start_times)
        self.assertIn(time(17, 30), start_times)
        self.assertIn(time(18, 0), start_times)
        self.assertIn(time(18, 30), start_times)

        self.assertEqual(7, len(start_times))

    def test_one_and_half_hour_period(self):
        start_times = get_available_start_times_for_given_duration_and_date(duration_in_hours='1.5', tr_day_date=date)

        self.assertIn(time(10, 0), start_times)
        self.assertIn(time(17, 30), start_times)
        self.assertIn(time(18, 0), start_times)

        self.assertEqual(3, len(start_times))

    def test_two_hours_period(self):
        start_times = get_available_start_times_for_given_duration_and_date(duration_in_hours='2.0', tr_day_date=date)

        self.assertIn(time(17, 30), start_times)
        self.assertEqual(1, len(start_times))


class TestOnlyOneHour(TestCase):
    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create(
            id=1, username='Nikita', first_name='Nikita', status=User.STATUS_TRAINING, password='123'
        )
        self.group = TrainingGroup.objects.create(name='Nikita_group', max_players=1, status=TrainingGroup.STATUS_4IND)

        self.tr_day_8__10 = create_tr_day_for_group(self.group, time(8, 0), timedelta(hours=2))
        self.tr_day_10__12 = create_tr_day_for_group(self.group, time(10, 0), timedelta(hours=2))
        self.tr_day_1230__14 = create_tr_day_for_group(self.group, time(12, 30), timedelta(hours=1, minutes=30))
        self.tr_day_15__17 = create_tr_day_for_group(self.group, time(15, 0), timedelta(hours=2))
        self.tr_day_18__20 = create_tr_day_for_group(self.group, time(18, 0), timedelta(hours=2))

    def test_one_hour_period(self):
        start_times = get_available_start_times_for_given_duration_and_date(duration_in_hours='1.0', tr_day_date=date)
        print(f"period=1.0", start_times)

        self.assertIn(time(14, 0), start_times)
        self.assertIn(time(17, 0), start_times)
        self.assertIn(time(20, 0), start_times)

        self.assertEqual(3, len(start_times))

    def test_one_and_half_hour_period(self):
        start_times = get_available_start_times_for_given_duration_and_date(duration_in_hours='1.5', tr_day_date=date)
        print(f"period=1.5", start_times)
        self.assertEqual(0, len(start_times))

    def test_two_hours_period(self):
        start_times = get_available_start_times_for_given_duration_and_date(duration_in_hours='2.0', tr_day_date=date)
        print(f"period=2.0", start_times)
        self.assertEqual(0, len(start_times))


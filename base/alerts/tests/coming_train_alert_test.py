from datetime import datetime, date, timedelta

from django.test import TestCase

from base.models import GroupTrainingDay, Photo
from base.utils.for_tests import CreateData


class TestCases(TestCase):
    def test_get_tr_days_for_alerting(self) -> None:
        now = datetime.now()

        player = CreateData.group_player(tg_id=350490234, first_name="Nikita")

        group = CreateData.group()
        group.players.add(player)

        tr_day_10_days_ago = CreateData.tr_day_for_group(
            group, date=date.today() - timedelta(days=10)
        )

        hour_ago = now - timedelta(hours=1)
        tr_day_1_hour_ago = CreateData.tr_day_for_group(
            group, date=hour_ago.date(), start_time=hour_ago.time()
        )

        two_hours_ahead = now + timedelta(hours=2)
        tr_day_2_hours_ahead = CreateData.tr_day_for_group(
            group, date=two_hours_ahead.date(), start_time=two_hours_ahead.time()
        )

        seven_hours_ahead = now + timedelta(hours=7)
        tr_day_7_hours_ahead = CreateData.tr_day_for_group(
            group, date=seven_hours_ahead.date(), start_time=seven_hours_ahead.time()
        )

        tr_day_10_days_ahead = CreateData.tr_day_for_group(
            group, date=date.today() + timedelta(days=10)
        )

        tr_days_for_alert = list(
            GroupTrainingDay.get_tr_days_for_alerting_about_coming_train()
        )

        self.assertIn(tr_day_2_hours_ahead, tr_days_for_alert)
        self.assertNotIn(tr_day_10_days_ago, tr_days_for_alert)
        self.assertNotIn(tr_day_1_hour_ago, tr_days_for_alert)
        self.assertNotIn(tr_day_7_hours_ahead, tr_days_for_alert)
        self.assertNotIn(tr_day_10_days_ahead, tr_days_for_alert)

        self.assertEqual(1, len(tr_days_for_alert))

    def test_photos_for_alerts_exist(self):
        self.assertTrue(Photo.objects.exists())

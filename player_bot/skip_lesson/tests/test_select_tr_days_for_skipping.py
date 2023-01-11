from datetime import timedelta, datetime

from django.test import TestCase

from base.common_for_bots.utils import moscow_datetime
from base.models import TrainingGroup
from base.utils.for_tests import CreateData
from player_bot.skip_lesson.utils import select_tr_days_for_skipping


class SelectTrDaysForSkippingTestCases(TestCase):
    def setUp(self):
        self.player = CreateData.group_player(tg_id=1)

        self.player_group = CreateData.group()
        self.player_group.players.add(self.player)

        self.individual_group = TrainingGroup.get_or_create_ind_group(self.player)
        self.renting_group = TrainingGroup.get_or_create_rent_group(self.player)
        self.renting_group.players.add(self.player)
        self.individual_group.players.add(self.player)

    def test_cant_skip_trainings_in_past(self):
        # нельзя пропустить тренировки, которые уже прошли

        day_ago = (datetime.today() - timedelta(days=1)).date()
        group_tr_day = CreateData.tr_day_for_group(group=self.player_group, date=day_ago)
        ind_tr_day = CreateData.tr_day_for_group(group=self.individual_group, date=day_ago)
        rent_tr_day = CreateData.tr_day_for_group(group=self.renting_group, date=day_ago)

        tr_days_for_skipping = select_tr_days_for_skipping(self.player)

        self.assertNotIn(group_tr_day, tr_days_for_skipping)
        self.assertNotIn(ind_tr_day, tr_days_for_skipping)
        self.assertNotIn(rent_tr_day, tr_days_for_skipping)

        self.assertEqual(0, len(list(tr_days_for_skipping)))

    def test_cant_skip_if_in_absent(self):
        # нельзя пропустить, если игрок уже в absent

        group_tr_day = CreateData.tr_day_for_group(group=self.player_group)
        group_tr_day.absent.add(self.player)

        tr_days_for_skipping = select_tr_days_for_skipping(self.player)

        self.assertNotIn(group_tr_day, tr_days_for_skipping)

    def test_cant_skip_regard_time_before_cancel(self):
        # нельзя пропустить, если до тренировки осталось меньше, чем player.time_before_cancel (default = 6 hours)

        now = moscow_datetime(datetime.now())
        training_start = now + timedelta(hours=1)

        group_tr_day = CreateData.tr_day_for_group(group=self.player_group, date=training_start.date(), start_time=training_start.time())
        tr_days_for_skipping = select_tr_days_for_skipping(self.player)

        self.assertNotIn(group_tr_day, tr_days_for_skipping)

    def test_can_skip_train_in_future(self):
        # можно пропустить, если тренировка в будущем

        group_tr_day = CreateData.tr_day_for_group(group=self.player_group)
        tr_days_for_skipping = select_tr_days_for_skipping(self.player)
        self.assertIn(group_tr_day, tr_days_for_skipping)

    def test_cant_skip_unavailable_train(self):
        # нельзя пропустить занятие, если оно недоступно
        group_tr_day = CreateData.tr_day_for_group(group=self.player_group, is_available=False)
        tr_days_for_skipping = select_tr_days_for_skipping(self.player)
        self.assertNotIn(group_tr_day, tr_days_for_skipping)

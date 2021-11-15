from django.test import TestCase
from base.models import TrainingGroup, GroupTrainingDay, Player

from datetime import datetime, timedelta, time

from base.common_for_bots.utils import get_n_free_places


def create_group_player(id: int, first_name: str, **kwargs) -> Player:
    player = Player.objects.create(tg_id=id, first_name=first_name, status=Player.STATUS_TRAINING, **kwargs)
    return player


def create_arbitrary_player(id: int, first_name: str, **kwargs) -> Player:
    player = Player.objects.create(tg_id=id, first_name=first_name, status=Player.STATUS_ARBITRARY, **kwargs)
    return player


def create_group(
        name="БАНДА №1", max_players=6, status=TrainingGroup.STATUS_GROUP, level=TrainingGroup.LEVEL_GREEN, **kwargs
    ) -> TrainingGroup:
    group = TrainingGroup.objects.create(
        name=name, max_players=max_players, status=status, level=level, **kwargs
    )
    return group


def create_tr_day_for_group(group, **kwargs):
    today = datetime.today()
    date = (today + timedelta(days=2)).date()
    tr_day = GroupTrainingDay.objects.create(
        group=group, date=date, start_time=time(9, 30), **kwargs
    )
    return tr_day


class GetNumberOfFreePlaces(TestCase):
    def setUp(self):
        self.player_1 = create_group_player(id=1, first_name='player_1')
        self.player_2 = create_group_player(id=2, first_name='player_2')
        self.player_3 = create_group_player(id=3, first_name='player_3')
        self.player_4 = create_group_player(id=4, first_name='player_4')
        self.player_5 = create_group_player(id=5, first_name='player_5')
        self.player_6 = create_group_player(id=6, first_name='player_6')
        self.player_7 = create_group_player(id=7, first_name='player_7')
        self.player_8 = create_group_player(id=8, first_name='player_8')
        self.player_9 = create_group_player(id=9, first_name='player_9')

    def test_no_places(self):
        group_4_max_players = create_group(max_players=4)
        group_6_max_players = create_group(max_players=6)
        group_4_max_players.players.add(self.player_1, self.player_2, self.player_3, self.player_4)
        group_6_max_players.players.add(self.player_1, self.player_2, self.player_3, self.player_4, self.player_5, self.player_6)

        tr_day_4 = create_tr_day_for_group(group_4_max_players)
        tr_day_4.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_4.visitors.add(self.player_5)
        tr_day_4.pay_visitors.add(self.player_6)
        tr_day_4.pay_bonus_visitors.add(self.player_7)

        tr_day_6 = create_tr_day_for_group(group_6_max_players)
        tr_day_6.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_6.visitors.add(self.player_7)
        tr_day_6.pay_visitors.add(self.player_8)
        tr_day_6.pay_bonus_visitors.add(self.player_9)

        self.assertEqual(0, get_n_free_places(tr_day_4))
        self.assertEqual(0, get_n_free_places(tr_day_6))

    def test_one_free_place(self):
        group_4_max_players = create_group(max_players=4)
        group_6_max_players = create_group(max_players=6)
        group_4_max_players.players.add(self.player_1, self.player_2, self.player_3, self.player_4)
        group_6_max_players.players.add(self.player_1, self.player_2, self.player_3, self.player_4, self.player_5, self.player_6)

        tr_day_4 = create_tr_day_for_group(group_4_max_players)
        tr_day_4.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_4.pay_visitors.add(self.player_6)
        tr_day_4.pay_bonus_visitors.add(self.player_7)

        tr_day_6 = create_tr_day_for_group(group_6_max_players)
        tr_day_6.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_6.pay_visitors.add(self.player_8)
        tr_day_6.pay_bonus_visitors.add(self.player_9)

        self.assertEqual(1, get_n_free_places(tr_day_4))
        self.assertEqual(1, get_n_free_places(tr_day_6))

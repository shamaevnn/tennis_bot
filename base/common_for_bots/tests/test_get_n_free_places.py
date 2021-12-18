from django.test import TestCase

from base.common_for_bots.utils import get_n_free_places
from base.utils.for_tests import CreateData


class GetNumberOfFreePlaces(TestCase):
    def setUp(self):
        self.player_1 = CreateData.group_player(tg_id=1, first_name="player_1")
        self.player_2 = CreateData.group_player(tg_id=2, first_name="player_2")
        self.player_3 = CreateData.group_player(tg_id=3, first_name="player_3")
        self.player_4 = CreateData.group_player(tg_id=4, first_name="player_4")
        self.player_5 = CreateData.group_player(tg_id=5, first_name="player_5")
        self.player_6 = CreateData.group_player(tg_id=6, first_name="player_6")
        self.player_7 = CreateData.group_player(tg_id=7, first_name="player_7")
        self.player_8 = CreateData.group_player(tg_id=8, first_name="player_8")
        self.player_9 = CreateData.group_player(tg_id=9, first_name="player_9")

    def test_no_places(self):
        group_4_max_players = CreateData.group(max_players=4)
        group_6_max_players = CreateData.group(max_players=6)
        group_4_max_players.players.add(
            self.player_1, self.player_2, self.player_3, self.player_4
        )
        group_6_max_players.players.add(
            self.player_1,
            self.player_2,
            self.player_3,
            self.player_4,
            self.player_5,
            self.player_6,
        )

        tr_day_4 = CreateData.tr_day_for_group(group_4_max_players)
        tr_day_4.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_4.visitors.add(self.player_5)
        tr_day_4.pay_visitors.add(self.player_6)
        tr_day_4.pay_bonus_visitors.add(self.player_7)

        tr_day_6 = CreateData.tr_day_for_group(group_6_max_players)
        tr_day_6.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_6.visitors.add(self.player_7)
        tr_day_6.pay_visitors.add(self.player_8)
        tr_day_6.pay_bonus_visitors.add(self.player_9)

        self.assertEqual(0, get_n_free_places(tr_day_4))
        self.assertEqual(0, get_n_free_places(tr_day_6))

    def test_one_free_place(self):
        group_4_max_players = CreateData.group(max_players=4)
        group_6_max_players = CreateData.group(max_players=6)
        group_4_max_players.players.add(
            self.player_1, self.player_2, self.player_3, self.player_4
        )
        group_6_max_players.players.add(
            self.player_1,
            self.player_2,
            self.player_3,
            self.player_4,
            self.player_5,
            self.player_6,
        )

        tr_day_4 = CreateData.tr_day_for_group(group_4_max_players)
        tr_day_4.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_4.pay_visitors.add(self.player_6)
        tr_day_4.pay_bonus_visitors.add(self.player_7)

        tr_day_6 = CreateData.tr_day_for_group(group_6_max_players)
        tr_day_6.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_6.pay_visitors.add(self.player_8)
        tr_day_6.pay_bonus_visitors.add(self.player_9)

        self.assertEqual(1, get_n_free_places(tr_day_4))
        self.assertEqual(1, get_n_free_places(tr_day_6))

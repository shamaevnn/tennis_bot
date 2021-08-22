from django.test import TestCase
from base.models import User, TrainingGroup, GroupTrainingDay

from datetime import datetime, timedelta, time

from base.common_for_bots.utils import get_n_free_places


def create_group_user(id: int, first_name: str, **kwargs):
    user = User.objects.create(id=id, username=first_name, first_name=first_name, status=User.STATUS_TRAINING,
                               password='123', **kwargs)
    return user


def create_arbitrary_user(id: int, first_name: str, **kwargs):
    user = User.objects.create(id=id, username=first_name, first_name=first_name, status=User.STATUS_ARBITRARY,
                               password='123', **kwargs)
    return user


def create_group(
        name="БАНДА №1", max_players=6, status=TrainingGroup.STATUS_GROUP, level=TrainingGroup.LEVEL_GREEN, **kwargs
    ):
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
        self.user_1 = create_group_user(id=1, first_name='user_1')
        self.user_2 = create_group_user(id=2, first_name='user_2')
        self.user_3 = create_group_user(id=3, first_name='user_3')
        self.user_4 = create_group_user(id=4, first_name='user_4')
        self.user_5 = create_group_user(id=5, first_name='user_5')
        self.user_6 = create_group_user(id=6, first_name='user_6')
        self.user_7 = create_group_user(id=7, first_name='user_7')
        self.user_8 = create_group_user(id=8, first_name='user_8')
        self.user_9 = create_group_user(id=9, first_name='user_9')

    def test_no_places(self):
        group_4_max_players = create_group(max_players=4)
        group_6_max_players = create_group(max_players=6)
        group_4_max_players.users.add(self.user_1, self.user_2, self.user_3, self.user_4)
        group_6_max_players.users.add(self.user_1, self.user_2, self.user_3, self.user_4, self.user_5, self.user_6)

        tr_day_4 = create_tr_day_for_group(group_4_max_players)
        tr_day_4.absent.add(self.user_1, self.user_2, self.user_3)
        tr_day_4.visitors.add(self.user_5)
        tr_day_4.pay_visitors.add(self.user_6)
        tr_day_4.pay_bonus_visitors.add(self.user_7)

        tr_day_6 = create_tr_day_for_group(group_6_max_players)
        tr_day_6.absent.add(self.user_1, self.user_2, self.user_3)
        tr_day_6.visitors.add(self.user_7)
        tr_day_6.pay_visitors.add(self.user_8)
        tr_day_6.pay_bonus_visitors.add(self.user_9)

        self.assertEqual(0, get_n_free_places(tr_day_4))
        self.assertEqual(0, get_n_free_places(tr_day_6))

    def test_one_free_place(self):
        group_4_max_players = create_group(max_players=4)
        group_6_max_players = create_group(max_players=6)
        group_4_max_players.users.add(self.user_1, self.user_2, self.user_3, self.user_4)
        group_6_max_players.users.add(self.user_1, self.user_2, self.user_3, self.user_4, self.user_5, self.user_6)

        tr_day_4 = create_tr_day_for_group(group_4_max_players)
        tr_day_4.absent.add(self.user_1, self.user_2, self.user_3)
        tr_day_4.pay_visitors.add(self.user_6)
        tr_day_4.pay_bonus_visitors.add(self.user_7)

        tr_day_6 = create_tr_day_for_group(group_6_max_players)
        tr_day_6.absent.add(self.user_1, self.user_2, self.user_3)
        tr_day_6.pay_visitors.add(self.user_8)
        tr_day_6.pay_bonus_visitors.add(self.user_9)

        self.assertEqual(1, get_n_free_places(tr_day_4))
        self.assertEqual(1, get_n_free_places(tr_day_6))

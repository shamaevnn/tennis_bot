from datetime import datetime, timedelta

from django.test import TestCase
from base.models import User, TrainingGroup, GroupTrainingDay
from tele_interface.utils import get_potential_days_for_group_training


def create_group_user(id: int, first_name: str):
    user = User.objects.create(id=id, username=first_name, first_name=first_name, status=User.STATUS_TRAINING,
                               password='123')
    return user


def create_arbitrary_user(id: int, first_name: str):
    user = User.objects.create(id=id, username=first_name, first_name=first_name, status=User.STATUS_ARBITRARY,
                               password='123')
    return user


def create_group(name="БАНДА №1", max_players=6, status=TrainingGroup.STATUS_GROUP, level=TrainingGroup.LEVEL_GREEN, **kwargs):
    group = TrainingGroup.objects.create(
        name=name, max_players=max_players, status=status, level=level, **kwargs
    )
    return group


def create_tr_day_for_group(group, **kwargs):
    today = datetime.today()
    tr_day = GroupTrainingDay.objects.create(
        group=group, date=today + timedelta(days=1), start_time="09:30:00", **kwargs
    )
    return tr_day


class BaseTestCases(TestCase):
    def setUp(self):
        self.me_training_in_group = create_group_user(id=350490234, first_name='Nikita 1')
        self.user_1 = create_group_user(id=1, first_name='user_1')
        self.user_2 = create_group_user(id=2, first_name='user_2')

    def test_no_individual(self):
        # нельзя записаться на индивидуальную тренировку
        group = create_group(name='ASdrqw', status=TrainingGroup.STATUS_4IND)

        tr_day = create_tr_day_for_group(group=group, is_individual=True)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)

    def test_no_1_max_players(self):
        # нельзя записаться в группу, если там максимум 1 игрок.
        # Даже если статус групповой и не индивидуальная тренировка
        group = create_group()
        tr_day = create_tr_day_for_group(group)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)

    def test_not_available(self):
        # нельзя записаться в день, если is_available=False
        group = create_group()
        tr_day = create_tr_day_for_group(group, is_available=False)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)

    def test_not_my_group(self):
        # нельзя записаться в свою группу
        group_with_me = create_group(max_players=4)
        group_with_me.users.add(self.me_training_in_group, self.user_1, self.user_2)

        tr_day = create_tr_day_for_group(group=group_with_me)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)

    def test_not_visitors(self):
        # нельзя записаться в группу, если пользователь уже в visitors
        group = create_group()

        tr_day = create_tr_day_for_group(group)
        tr_day.visitors.add(self.me_training_in_group)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)

    def test_not_pay_visitors(self):
        # нельзя записаться в группу, если пользователь уже в pay_visitors
        group = create_group()

        tr_day = create_tr_day_for_group(group)
        tr_day.pay_visitors.add(self.me_training_in_group)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)

    def test_not_pay_bonus_visitors(self):
        # нельзя записаться в группу, если пользователь уже в pay_bonus_visitors
        group = create_group()

        tr_day = create_tr_day_for_group(group)
        tr_day.pay_bonus_visitors.add(self.me_training_in_group)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)


class NotAvailableForAdditionalLessonsTestCases(TestCase):
    def setUp(self):
        self.me_training_in_group = create_group_user(id=350490234, first_name='Nikita')

        self.user_1 = create_group_user(id=1, first_name='user_1')
        self.user_2 = create_group_user(id=2, first_name='user_2')
        self.user_3 = create_group_user(id=3, first_name='user_3')
        self.user_4 = create_group_user(id=4, first_name='user_4')
        self.user_5 = create_group_user(id=5, first_name='user_5')
        self.user_6 = create_group_user(id=6, first_name='user_6')
        self.user_7 = create_group_user(id=7, first_name='user_7')

        self.group_with_4_players = create_group(name="Банда №1", max_players=4)
        self.group_with_6_players = create_group(name="Банда №2", max_players=6)

        self.group_with_4_players.users.add(self.user_1, self.user_2, self.user_3, self.user_4)
        self.group_with_6_players.users.add(self.user_1, self.user_2, self.user_3, self.user_4, self.user_5, self.user_6)

    def test_all_users_from_group(self):
        # нельзя записаться, если присутствуют все из группы и max_players=count(users)
        tr_day = create_tr_day_for_group(self.group_with_4_players)
        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)

    def test_when_full_with_absents_and_visitors(self):
        # нельзя записаться, если все места заняты, есть отсутствующие и посетители из других групп
        tr_day = create_tr_day_for_group(self.group_with_4_players)
        tr_day.absent.add(self.user_1, self.user_2)
        tr_day.visitors.add(self.user_5, self.user_6)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)

    def test_when_full_with_absents_and_all_kind_of_visitors(self):
        # нельзя записаться, если все места заняты, есть отсутствующие и различные посетители
        tr_day = create_tr_day_for_group(self.group_with_4_players)
        tr_day.absent.add(self.user_1, self.user_2, self.user_3)
        tr_day.visitors.add(self.user_5)
        tr_day.pay_visitors.add(self.user_6)
        tr_day.pay_bonus_visitors.add(self.user_7)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertNotIn(tr_day, days)

    def test_one_absent(self):
        # можно записаться, если есть один отсутствующий
        tr_day = create_tr_day_for_group(self.group_with_4_players)
        tr_day.absent.add(self.user_1)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertIn(tr_day, days)

    def test_absent_with_all_kind_of_visitors(self):
        # можно записаться, если есть отсутствующие, посетители и есть места
        tr_day = create_tr_day_for_group(self.group_with_4_players)
        tr_day.absent.add(self.user_1, self.user_2, self.user_3)
        tr_day.visitors.add(self.user_4)
        tr_day.pay_bonus_visitors.add(self.user_5)

        days = get_potential_days_for_group_training(user=self.me_training_in_group)
        self.assertIn(tr_day, days)
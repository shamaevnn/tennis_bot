from datetime import datetime, timedelta

from django.test import TestCase

from base.models import TrainingGroup, GroupTrainingDay
from base.utils.for_tests import CreateData
from player_bot.skip_lesson.static_text import (
    PLAYER_CANCELLED_IND_TRAIN,
    PLAYER_SKIPPED_TRAIN_FOR_BONUS,
    PLAYER_SKIPPED_TRAIN_FOR_MONEY,
    PLAYER_SKIPPED_TRAIN_FOR_PAY_BONUS,
    PLAYER_SKIPPED_TRAIN_IN_HIS_GROUP,
    OKAY_TRAIN_CANCELLED,
    PLAYER_CANCELLED_RENT_COURT,
)
from base.common_for_bots.static_text import ATTENTION
from player_bot.skip_lesson.utils import handle_skipping_train


class HandleSkippingTrainTestCases(TestCase):
    def setUp(self):
        self.date_info = ""
        self.success_cancel_text = OKAY_TRAIN_CANCELLED.format(self.date_info)
        self.me = CreateData.group_player(tg_id=1, first_name="Nikita")

    # todo: добавить тест для time_before_cancel
    def test_ind_group(self):
        self.individual_group = TrainingGroup.get_or_create_ind_group(self.me)
        self.individual_group.players.add(self.me)

        self.tr_day_individual_1 = CreateData.tr_day_for_group(
            self.individual_group, status=GroupTrainingDay.INDIVIDUAL_TRAIN
        )
        self.tr_day_individual_2 = CreateData.tr_day_for_group(
            group=self.individual_group,
            date=(datetime.today() + timedelta(days=3)).date(),
            status=GroupTrainingDay.INDIVIDUAL_TRAIN,
        )
        self.tr_day_individual_3 = CreateData.tr_day_for_group(
            group=self.individual_group,
            date=(datetime.today() + timedelta(days=4)).date(),
            status=GroupTrainingDay.INDIVIDUAL_TRAIN,
        )

        # если тренировка индивидуальная, то запись удаляется
        # тренировки есть в расписании
        self.assertIn(self.tr_day_individual_1, GroupTrainingDay.objects.all())
        self.assertIn(self.tr_day_individual_2, GroupTrainingDay.objects.all())
        self.assertIn(self.tr_day_individual_3, GroupTrainingDay.objects.all())

        # обрабатываем пропуск
        player_text, admin_text = handle_skipping_train(
            self.tr_day_individual_1, self.me, self.date_info
        )
        # проверяем, что тренировка удалилась
        self.assertTrue(self.tr_day_individual_1.is_deleted)

        # создались нужные тексты для тренера и игроков
        self.assertEqual(player_text, self.success_cancel_text)
        self.assertEqual(
            admin_text,
            PLAYER_CANCELLED_IND_TRAIN.format(
                ATTENTION, self.me.first_name, self.me.last_name, self.date_info
            ),
        )

        # другие индивидуальные тренировки не удаляются
        self.assertFalse(self.tr_day_individual_2.is_deleted)
        self.assertFalse(self.tr_day_individual_3.is_deleted)

    def test_rent_group(self):
        self.renting_group = TrainingGroup.get_or_create_rent_group(self.me)
        self.renting_group.players.add(self.me)

        self.tr_day_rent_court = CreateData.tr_day_for_group(
            self.renting_group, status=GroupTrainingDay.RENT_COURT_STATUS
        )
        self.tr_day_rent_court_2 = GroupTrainingDay.objects.create(
            group=self.renting_group,
            date=(datetime.today() + timedelta(days=4)).date(),
            status=GroupTrainingDay.RENT_COURT_STATUS,
        )

        # если это аренда, то запись удаляется
        self.assertIn(self.tr_day_rent_court, GroupTrainingDay.objects.all())
        text, admin_text = handle_skipping_train(
            self.tr_day_rent_court, self.me, self.date_info
        )
        self.assertTrue(self.tr_day_rent_court.is_deleted)

        # создались нужные тексты для тренера и игроков
        self.assertEqual(text, self.success_cancel_text)
        self.assertEqual(
            admin_text,
            PLAYER_CANCELLED_RENT_COURT.format(
                ATTENTION, self.me.first_name, self.me.last_name, self.date_info
            ),
        )

        # другая аренда не удаляется
        self.assertFalse(self.tr_day_rent_court_2.is_deleted)

    def test_my_group(self):
        self.my_group = CreateData.group()
        self.my_group.players.add(self.me)
        self.tr_day = CreateData.tr_day_for_group(self.my_group)

        # прибавляется отыгрыш и игрок заносится в absent
        current_bonus_lessons = self.me.bonus_lesson
        text, admin_text = handle_skipping_train(self.tr_day, self.me, self.date_info)
        self.assertEqual(text, self.success_cancel_text)
        self.assertEqual(
            admin_text,
            PLAYER_SKIPPED_TRAIN_IN_HIS_GROUP.format(
                self.me.first_name, self.me.last_name, self.date_info
            ),
        )
        self.assertIn(self.me, self.tr_day.absent.all())
        self.assertEqual(self.me.bonus_lesson, current_bonus_lessons + 1)

    def test_visitor(self):
        self.not_my_group_1 = CreateData.group()
        self.tr_day_visitor = CreateData.tr_day_for_group(self.not_my_group_1)
        self.tr_day_visitor.visitors.add(self.me)

        # прибавляется отыгрыш и игрок убирается из visitors
        current_bonus_lessons = self.me.bonus_lesson
        self.assertIn(self.me, self.tr_day_visitor.visitors.all())
        text, admin_text = handle_skipping_train(
            self.tr_day_visitor, self.me, self.date_info
        )
        self.assertEqual(text, self.success_cancel_text)
        self.assertEqual(
            admin_text,
            PLAYER_SKIPPED_TRAIN_FOR_BONUS.format(
                self.me.first_name, self.me.last_name, self.date_info
            ),
        )
        self.assertNotIn(self.me, self.tr_day_visitor.visitors.all())
        self.assertEqual(self.me.bonus_lesson, current_bonus_lessons + 1)

    def test_pay_visitor(self):
        self.not_my_group_2 = CreateData.group()
        self.tr_day_pay_visitor = CreateData.tr_day_for_group(self.not_my_group_2)

        self.tr_day_pay_visitor.pay_visitors.add(self.me)

        # прибавляется отыгрыш и игрок убирается из pay_visitors
        current_bonus_lessons = self.me.bonus_lesson
        self.assertIn(self.me, self.tr_day_pay_visitor.pay_visitors.all())
        text, admin_text = handle_skipping_train(
            self.tr_day_pay_visitor, self.me, self.date_info
        )
        self.assertEqual(text, self.success_cancel_text)
        self.assertEqual(
            admin_text,
            PLAYER_SKIPPED_TRAIN_FOR_MONEY.format(
                self.me.first_name, self.me.last_name, self.date_info
            ),
        )
        self.assertNotIn(self.me, self.tr_day_pay_visitor.pay_visitors.all())
        self.assertEqual(self.me.bonus_lesson, current_bonus_lessons)

    def test_pay_bonus_visitor(self):
        self.not_my_group_3 = CreateData.group()
        self.tr_day_pay_bonus_visitor = CreateData.tr_day_for_group(self.not_my_group_3)
        self.tr_day_pay_bonus_visitor.pay_bonus_visitors.add(self.me)

        # прибавляется отыгрыш и игрок убирается из pay_bonus_visitor
        current_bonus_lessons = self.me.bonus_lesson
        self.assertIn(self.me, self.tr_day_pay_bonus_visitor.pay_bonus_visitors.all())
        text, admin_text = handle_skipping_train(
            self.tr_day_pay_bonus_visitor, self.me, self.date_info
        )
        self.assertEqual(text, self.success_cancel_text)
        self.assertEqual(
            admin_text,
            PLAYER_SKIPPED_TRAIN_FOR_PAY_BONUS.format(
                self.me.first_name, self.me.last_name, self.date_info
            ),
        )
        self.assertNotIn(
            self.me, self.tr_day_pay_bonus_visitor.pay_bonus_visitors.all()
        )
        self.assertEqual(self.me.bonus_lesson, current_bonus_lessons + 1)

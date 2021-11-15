from datetime import time, datetime, timedelta

from django.test import TestCase

from base.models import TrainingGroup, GroupTrainingDay
from player_bot.skip_lesson.static_text import USER_CANCELLED_IND_TRAIN, USER_SKIPPED_TRAIN_FOR_BONUS, \
	USER_SKIPPED_TRAIN_FOR_MONEY, USER_SKIPPED_TRAIN_FOR_PAY_BONUS, USER_SKIPPED_TRAIN_IN_HIS_GROUP, \
	OKAY_TRAIN_CANCELLED, USER_CANCELLED_RENT_COURT
from base.common_for_bots.static_text import ATTENTION
from player_bot.take_lesson.tests.test_get_potential_days_for_group_training import create_group_player, \
create_group, create_tr_day_for_group
from player_bot.skip_lesson.utils import handle_skipping_train


class HandleSkippingTrainTestCases(TestCase):
	def setUp(self):
		self.date_info = ""
		self.success_cancel_text = OKAY_TRAIN_CANCELLED.format(self.date_info)

		self.me = create_group_player(id=1, first_name='Nikita')
		self.my_group = create_group()
		self.my_group.users.add(self.me)
		self.individual_group = TrainingGroup.get_or_create_ind_group(self.me)
		self.renting_group = TrainingGroup.get_or_create_rent_group(self.me)

		self.renting_group.users.add(self.me)
		self.individual_group.users.add(self.me)

		self.not_my_group_1 = create_group()
		self.not_my_group_2 = create_group()
		self.not_my_group_3 = create_group()

		self.tr_day = create_tr_day_for_group(self.my_group)
		self.tr_day_visitor = create_tr_day_for_group(self.not_my_group_1)
		self.tr_day_pay_visitor = create_tr_day_for_group(self.not_my_group_2)
		self.tr_day_pay_bonus_visitor = create_tr_day_for_group(self.not_my_group_3)
		self.tr_day_individual_1 = create_tr_day_for_group(self.individual_group, is_individual=True)
		self.tr_day_individual_2 = GroupTrainingDay.objects.create(
			group=self.individual_group, start_time=time(14, 30), date=(datetime.today() + timedelta(days=2)).date(),
			is_individual=True
		)
		self.tr_day_rent_court = create_tr_day_for_group(
			self.renting_group, tr_day_status=GroupTrainingDay.RENT_COURT_STATUS
		)
		self.tr_day_rent_court_2 = GroupTrainingDay.objects.create(
			group=self.renting_group, start_time=time(14, 30), date=(datetime.today() + timedelta(days=2)).date(),
			tr_day_status=GroupTrainingDay.RENT_COURT_STATUS,
		)

		self.tr_day_visitor.visitors.add(self.me)
		self.tr_day_pay_visitor.pay_visitors.add(self.me)
		self.tr_day_pay_bonus_visitor.pay_bonus_visitors.add(self.me)

	# todo: добавить тест для time_before_cancel
	def test_ind_group(self):
		# если тренировка индивидуальная, то запись удаляется
		self.assertIn(self.tr_day_individual_1, GroupTrainingDay.objects.all())
		text, admin_text = handle_skipping_train(self.tr_day_individual_1, self.me, self.date_info)
		self.assertNotIn(self.tr_day_individual_1, GroupTrainingDay.objects.all())

		# создались нужные тексты для тренера и игроков
		self.assertEqual(text, self.success_cancel_text)
		self.assertEqual(
			admin_text,
			USER_CANCELLED_IND_TRAIN.format(
				ATTENTION, self.me.first_name, self.me.last_name, self.date_info
			)
		)

		# другая индивидуальная тренировка не удаляется
		self.assertIn(self.tr_day_individual_2, GroupTrainingDay.objects.all())

	def test_rent_group(self):
		# если это аренда, то запись удаляется
		self.assertIn(self.tr_day_rent_court, GroupTrainingDay.objects.all())
		text, admin_text = handle_skipping_train(self.tr_day_rent_court, self.me, self.date_info)
		self.assertNotIn(self.tr_day_rent_court, GroupTrainingDay.objects.all())

		# создались нужные тексты для тренера и игроков
		self.assertEqual(text, self.success_cancel_text)
		self.assertEqual(
			admin_text,
			USER_CANCELLED_RENT_COURT.format(
				ATTENTION, self.me.first_name, self.me.last_name, self.date_info
			)
		)

		# другая аренда не удаляется
		self.assertIn(self.tr_day_rent_court_2, GroupTrainingDay.objects.all())

	def test_my_group(self):
		# прибавляется отыгрыш и игрок заносится в absent
		current_bonus_lessons = self.me.bonus_lesson
		text, admin_text = handle_skipping_train(self.tr_day, self.me, self.date_info)
		self.assertEqual(text, self.success_cancel_text)
		self.assertEqual(
			admin_text,
			USER_SKIPPED_TRAIN_IN_HIS_GROUP.format(self.me.first_name, self.me.last_name, self.date_info)
		)
		self.assertIn(self.me, self.tr_day.absent.all())
		self.assertEqual(self.me.bonus_lesson, current_bonus_lessons + 1)

	def test_visitor(self):
		# прибавляется отыгрыш и игрок убирается из visitors
		current_bonus_lessons = self.me.bonus_lesson
		self.assertIn(self.me, self.tr_day_visitor.visitors.all())
		text, admin_text = handle_skipping_train(self.tr_day_visitor, self.me, self.date_info)
		self.assertEqual(text, self.success_cancel_text)
		self.assertEqual(
			admin_text,
			USER_SKIPPED_TRAIN_FOR_BONUS.format(self.me.first_name, self.me.last_name, self.date_info)
		)
		self.assertNotIn(self.me, self.tr_day_visitor.visitors.all())
		self.assertEqual(self.me.bonus_lesson, current_bonus_lessons + 1)

	def test_pay_visitor(self):
		# прибавляется отыгрыш и игрок убирается из pay_visitors
		current_bonus_lessons = self.me.bonus_lesson
		self.assertIn(self.me, self.tr_day_pay_visitor.pay_visitors.all())
		text, admin_text = handle_skipping_train(self.tr_day_pay_visitor, self.me, self.date_info)
		self.assertEqual(text, self.success_cancel_text)
		self.assertEqual(
			admin_text,
			USER_SKIPPED_TRAIN_FOR_MONEY.format(self.me.first_name, self.me.last_name, self.date_info)
		)
		self.assertNotIn(self.me, self.tr_day_pay_visitor.pay_visitors.all())
		self.assertEqual(self.me.bonus_lesson, current_bonus_lessons)

	def test_pay_bonus_visitor(self):
		# прибавляется отыгрыш и игрок убирается из pay_bonus_visitor
		current_bonus_lessons = self.me.bonus_lesson
		self.assertIn(self.me, self.tr_day_pay_bonus_visitor.pay_bonus_visitors.all())
		text, admin_text = handle_skipping_train(self.tr_day_pay_bonus_visitor, self.me, self.date_info)
		self.assertEqual(text, self.success_cancel_text)
		self.assertEqual(
			admin_text,
			USER_SKIPPED_TRAIN_FOR_PAY_BONUS.format(self.me.first_name, self.me.last_name, self.date_info)
		)
		self.assertNotIn(self.me, self.tr_day_pay_bonus_visitor.pay_bonus_visitors.all())
		self.assertEqual(self.me.bonus_lesson, current_bonus_lessons + 1)







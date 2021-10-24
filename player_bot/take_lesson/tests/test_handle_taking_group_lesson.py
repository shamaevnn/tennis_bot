from datetime import datetime, timedelta, time

from django.test import TestCase

from base.common_for_bots.utils import get_n_free_places
from base.models import User, TrainingGroup, GroupTrainingDay
from player_bot.take_lesson.static_text import NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER, CHOOSE_TYPE_OF_PAYMENT
from player_bot.take_lesson.keyboard_utils import back_to_group_times_when_no_left_keyboard, \
    choose_type_of_payment_for_group_lesson_keyboard
from player_bot.take_lesson.utils import handle_taking_group_lesson
from tennis_bot.settings import TARIF_PAYMENT_ADD_LESSON, TARIF_GROUP, TARIF_ARBITRARY


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


class NoFreePlacesTests(TestCase):
    def assert_no_places_choose_another(self, user_text, user_markup, admin_text, admin_markup, tr_day):
        self.assertEqual(user_text, NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER)
        self.assertEqual(
            user_markup, back_to_group_times_when_no_left_keyboard(
                year=tr_day.date.year,
                month=tr_day.date.month,
                day=tr_day.date.day
            )
        )
        self.assertEqual(admin_text, '')
        self.assertIsNone(admin_markup)

    def setUp(self):
        # gr = group, u = user, w = with, wo = without, bl = bonus lesson, mp = max players,
        # al = additional lesson
        self.gr_u_w_bl = create_group_user(id=350490234, first_name='Nikita 1', bonus_lesson=10)
        self.gr_u_wo_bl = create_group_user(id=350490235, first_name='Nikita 2', bonus_lesson=0)
        self.arb_u_w_bl = create_arbitrary_user(id=350490236, first_name='Nikita 3', bonus_lesson=10)
        self.arb_u_wo_bl = create_arbitrary_user(id=350490236, first_name='Nikita 4', bonus_lesson=0)

        self.user_1 = create_group_user(id=1, first_name='user_1')
        self.user_2 = create_group_user(id=2, first_name='user_2')
        self.user_3 = create_group_user(id=3, first_name='user_3')
        self.user_4 = create_group_user(id=4, first_name='user_4')
        self.user_5 = create_group_user(id=5, first_name='user_5')
        self.user_6 = create_group_user(id=6, first_name='user_6')
        self.user_7 = create_group_user(id=7, first_name='user_7')
        self.user_8 = create_group_user(id=8, first_name='user_8')
        self.user_9 = create_group_user(id=9, first_name='user_9')

        self.gr_4_mp = create_group(max_players=4)
        self.gr_6_mp = create_group(max_players=6)
        self.gr_4_mp.users.add(self.user_1, self.user_2, self.user_3, self.user_4)
        self.gr_6_mp.users.add(self.user_1, self.user_2, self.user_3, self.user_4, self.user_5, self.user_6)

        self.gr_4_mp_al = create_group(max_players=4, available_for_additional_lessons=True)
        self.gr_5_mp_al = create_group(max_players=5, available_for_additional_lessons=True)
        self.gr_6_mp_al = create_group(max_players=6, available_for_additional_lessons=True)
        self.gr_4_mp_al.users.add(self.user_1, self.user_2, self.user_3, self.user_4)
        self.gr_5_mp_al.users.add(self.user_1, self.user_2, self.user_3, self.user_4, self.user_5)
        self.gr_6_mp_al.users.add(self.user_1, self.user_2, self.user_3, self.user_4, self.user_5, self.user_6)

    def test_no_free_places_no_additional_lessons(self):
        tr_day_4 = create_tr_day_for_group(self.gr_4_mp)
        tr_day_6 = create_tr_day_for_group(self.gr_6_mp)

        # все игроки из группы придут на занятие и нельзя записаться на доп. места
        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_4)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_4)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_4)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_4)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_4)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_4)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_4)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_4)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_6)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_6)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_6)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_6)

    def test_no_free_places_with_all_kinds_of_visitors_and_available_additional_lessons(self):
        tr_day_4 = create_tr_day_for_group(self.gr_4_mp_al)
        tr_day_4.absent.add(self.user_1, self.user_2, self.user_3)
        tr_day_4.visitors.add(self.user_5)
        tr_day_4.pay_visitors.add(self.user_6)
        tr_day_4.pay_bonus_visitors.add(self.user_7)

        tr_day_6 = create_tr_day_for_group(self.gr_6_mp_al)
        tr_day_6.absent.add(self.user_1, self.user_2, self.user_3)
        tr_day_6.visitors.add(self.user_7)
        tr_day_6.pay_visitors.add(self.user_8)
        tr_day_6.pay_bonus_visitors.add(self.user_9)

        # если есть отыгрыши, то должна появиться следующая клава с выбором типа оплаты:
        # за отыгрыш + деньги либо просто за деньги
        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_4)
        self.assertEqual(user_text, CHOOSE_TYPE_OF_PAYMENT)
        self.assertEqual(
            user_markup, choose_type_of_payment_for_group_lesson_keyboard(
                    payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                    tr_day_id=tr_day_4.id,
                    tarif=TARIF_GROUP,
            )
        )
        self.assertEqual(admin_text, '')
        self.assertIsNone(admin_markup)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_4)
        self.assertEqual(user_text, CHOOSE_TYPE_OF_PAYMENT)
        self.assertEqual(
            user_markup, choose_type_of_payment_for_group_lesson_keyboard(
                payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                tr_day_id=tr_day_4.id,
                tarif=TARIF_ARBITRARY,
            )
        )
        self.assertEqual(admin_text, '')
        self.assertIsNone(admin_markup)

        # если нет отыгрышей, то добавляем пользователя в pay_visitors и соответствующие texts
        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_4)
        self.assertIn(f"Не забудь заплатить <b>{TARIF_GROUP}₽</b>", user_text)
        self.assertIn(f"<b>не за счет отыгрышей, не забудь взять {TARIF_GROUP}₽.</b>", admin_text)
        self.assertIsNone(user_markup)
        self.assertIsNone(admin_markup)
        self.assertIn(self.gr_u_wo_bl, tr_day_4.pay_visitors.all())

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_4)
        self.assertIn(f"Не забудь заплатить <b>{TARIF_ARBITRARY}₽</b>", user_text)
        self.assertIn(f"<b>не за счет отыгрышей, не забудь взять {TARIF_ARBITRARY}₽.</b>", admin_text)
        self.assertIsNone(user_markup)
        self.assertIsNone(admin_markup)
        self.assertIn(self.arb_u_wo_bl, tr_day_4.pay_visitors.all())

        # если максимум 6 игроков и все места заняты, то нужно предлагать другое время
        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_6)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_6)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_6)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_6)

    def test_full_group_one_pay_plus_one(self):
        # additional_lessons=True, группа из 5 человек, один записался за деньги,
        # второй хочет записаться за платные отыгрыши, не можем записать, т.к. максимум 6 человек на занятии.
        # надо предлагать другое время.

        tr_day_5 = create_tr_day_for_group(self.gr_5_mp_al)
        tr_day_5.pay_visitors.add(self.user_6)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_5)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_5)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_5)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_5)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_5)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_5)

        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_5)
        self.assert_no_places_choose_another(user_text, user_markup, admin_text, admin_markup, tr_day_5)

    def test_take_lesson_in_my_group(self):
        # если игрок в отсутствующих, то он может опять записаться.
        # ему добавиться отыгрыш + уберется из absent
        tr_day_4 = create_tr_day_for_group(self.gr_4_mp_al)
        tr_day_4.absent.add(self.user_1)

        bonus_lesson_before = self.user_1.bonus_lesson
        user_text, user_markup, admin_text, admin_markup = handle_taking_group_lesson(self.user_1, tr_day_4)

        self.assertIsNone(user_markup)
        self.assertIsNone(admin_markup)

        self.user_1.refresh_from_db()
        self.assertEqual(self.user_1.bonus_lesson, bonus_lesson_before + 1)

        self.assertNotIn(self.user_1, tr_day_4.absent.all())

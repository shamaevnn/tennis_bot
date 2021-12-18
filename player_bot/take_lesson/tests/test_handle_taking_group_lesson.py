from django.test import TestCase

from base.utils.for_tests import CreateData
from player_bot.take_lesson.static_text import (
    NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER,
    CHOOSE_TYPE_OF_PAYMENT,
)
from player_bot.take_lesson.group.keyboards import (
    choose_type_of_payment_for_group_lesson_keyboard,
    back_to_group_times_when_no_left_keyboard,
)
from player_bot.take_lesson.group.utils import handle_taking_group_lesson
from tennis_bot.settings import TARIF_PAYMENT_ADD_LESSON, TARIF_GROUP, TARIF_ARBITRARY


class NoFreePlacesTests(TestCase):
    def assert_no_places_choose_another(
        self, player_text, player_markup, admin_text, admin_markup, tr_day
    ):
        self.assertEqual(player_text, NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER)
        self.assertEqual(
            player_markup,
            back_to_group_times_when_no_left_keyboard(
                year=tr_day.date.year, month=tr_day.date.month, day=tr_day.date.day
            ),
        )
        self.assertEqual(admin_text, "")
        self.assertIsNone(admin_markup)

    def setUp(self):
        # gr = group, u = user, w = with, wo = without, bl = bonus lesson, mp = max players,
        # al = additional lesson
        self.gr_u_w_bl = CreateData.group_player(
            tg_id=350490234, first_name="Nikita 1", bonus_lesson=10
        )
        self.gr_u_wo_bl = CreateData.group_player(
            tg_id=350490235, first_name="Nikita 2", bonus_lesson=0
        )
        self.arb_u_w_bl = CreateData.arbitrary_player(
            tg_id=350490236, first_name="Nikita 3", bonus_lesson=10
        )
        self.arb_u_wo_bl = CreateData.arbitrary_player(
            tg_id=350490236, first_name="Nikita 4", bonus_lesson=0
        )

        self.player_1 = CreateData.group_player(tg_id=1, first_name="player_1")
        self.player_2 = CreateData.group_player(tg_id=2, first_name="player_2")
        self.player_3 = CreateData.group_player(tg_id=3, first_name="player_3")
        self.player_4 = CreateData.group_player(tg_id=4, first_name="player_4")
        self.player_5 = CreateData.group_player(tg_id=5, first_name="player_5")
        self.player_6 = CreateData.group_player(tg_id=6, first_name="player_6")
        self.player_7 = CreateData.group_player(tg_id=7, first_name="player_7")
        self.player_8 = CreateData.group_player(tg_id=8, first_name="player_8")
        self.player_9 = CreateData.group_player(tg_id=9, first_name="player_9")

        self.gr_4_mp = CreateData.group(max_players=4)
        self.gr_6_mp = CreateData.group(max_players=6)
        self.gr_4_mp.players.add(
            self.player_1, self.player_2, self.player_3, self.player_4
        )
        self.gr_6_mp.players.add(
            self.player_1,
            self.player_2,
            self.player_3,
            self.player_4,
            self.player_5,
            self.player_6,
        )

        self.gr_4_mp_al = CreateData.group(
            max_players=4, available_for_additional_lessons=True
        )
        self.gr_5_mp_al = CreateData.group(
            max_players=5, available_for_additional_lessons=True
        )
        self.gr_6_mp_al = CreateData.group(
            max_players=6, available_for_additional_lessons=True
        )
        self.gr_4_mp_al.players.add(
            self.player_1, self.player_2, self.player_3, self.player_4
        )
        self.gr_5_mp_al.players.add(
            self.player_1, self.player_2, self.player_3, self.player_4, self.player_5
        )
        self.gr_6_mp_al.players.add(
            self.player_1,
            self.player_2,
            self.player_3,
            self.player_4,
            self.player_5,
            self.player_6,
        )

    def test_max_trainings_in_future(self):
        """
        Игрок gr_4_mp_al записался на 3 тренировки в будущем.
        Пытается записаться на tr_day_4. Нельзя сделать это, тк максимум тренировок в будущем = 3
        """
        tr_day_1 = CreateData.tr_day_for_group(self.gr_4_mp_al)
        tr_day_2 = CreateData.tr_day_for_group(self.gr_4_mp_al)
        tr_day_3 = CreateData.tr_day_for_group(self.gr_4_mp_al)
        tr_day_4 = CreateData.tr_day_for_group(self.gr_4_mp_al)
        tr_day_1.visitors.add(self.gr_u_w_bl)
        tr_day_2.pay_visitors.add(self.gr_u_w_bl)
        tr_day_3.pay_bonus_visitors.add(self.gr_u_w_bl)

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_4)
        self.assertIsNotNone(player_text)
        self.assertEqual(
            player_markup,
            back_to_group_times_when_no_left_keyboard(
                year=tr_day_4.date.year,
                month=tr_day_4.date.month,
                day=tr_day_4.date.day,
            ),
        )
        self.assertEqual(admin_text, "")
        self.assertIsNone(admin_markup)

    def test_no_free_places_no_additional_lessons(self):
        tr_day_4 = CreateData.tr_day_for_group(self.gr_4_mp)
        tr_day_6 = CreateData.tr_day_for_group(self.gr_6_mp)

        # все игроки из группы придут на занятие и нельзя записаться на доп. места
        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_4)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_4
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_4)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_4
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_4)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_4
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_4)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_4
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_6
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_6
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_6
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_6
        )

    def test_no_free_places_with_all_kinds_of_visitors_and_available_additional_lessons(
        self,
    ):
        tr_day_4 = CreateData.tr_day_for_group(self.gr_4_mp_al)
        tr_day_4.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_4.visitors.add(self.player_5)
        tr_day_4.pay_visitors.add(self.player_6)
        tr_day_4.pay_bonus_visitors.add(self.player_7)

        tr_day_6 = CreateData.tr_day_for_group(self.gr_6_mp_al)
        tr_day_6.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_6.visitors.add(self.player_7)
        tr_day_6.pay_visitors.add(self.player_8)
        tr_day_6.pay_bonus_visitors.add(self.player_9)

        # если есть отыгрыши, то должна появиться следующая клава с выбором типа оплаты:
        # за отыгрыш + деньги либо просто за деньги
        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_4)
        self.assertEqual(player_text, CHOOSE_TYPE_OF_PAYMENT)
        self.assertEqual(
            player_markup,
            choose_type_of_payment_for_group_lesson_keyboard(
                payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                tr_day_id=tr_day_4.id,
                tarif=TARIF_GROUP,
            ),
        )
        self.assertEqual(admin_text, "")
        self.assertIsNone(admin_markup)

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_4)
        self.assertEqual(player_text, CHOOSE_TYPE_OF_PAYMENT)
        self.assertEqual(
            player_markup,
            choose_type_of_payment_for_group_lesson_keyboard(
                payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                tr_day_id=tr_day_4.id,
                tarif=TARIF_ARBITRARY,
            ),
        )
        self.assertEqual(admin_text, "")
        self.assertIsNone(admin_markup)

        # если нет отыгрышей, то добавляем пользователя в pay_visitors и соответствующие texts
        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_4)
        self.assertIn(f"Не забудь заплатить <b>{TARIF_GROUP}₽</b>", player_text)
        self.assertIn(
            f"<b>не за счет отыгрышей, не забудь взять {TARIF_GROUP}₽.</b>", admin_text
        )
        self.assertIsNone(player_markup)
        self.assertIsNone(admin_markup)
        self.assertIn(self.gr_u_wo_bl, tr_day_4.pay_visitors.all())

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_4)
        self.assertIn(f"Не забудь заплатить <b>{TARIF_ARBITRARY}₽</b>", player_text)
        self.assertIn(
            f"<b>не за счет отыгрышей, не забудь взять {TARIF_ARBITRARY}₽.</b>",
            admin_text,
        )
        self.assertIsNone(player_markup)
        self.assertIsNone(admin_markup)
        self.assertIn(self.arb_u_wo_bl, tr_day_4.pay_visitors.all())

        # если максимум 6 игроков и все места заняты, то нужно предлагать другое время
        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_6
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_6
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_6
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_6
        )

    def test_full_group_one_pay_plus_one(self):
        # additional_lessons=True, группа из 5 человек, один записался за деньги,
        # второй хочет записаться за платные отыгрыши, не можем записать, т.к. максимум 6 человек на занятии.
        # надо предлагать другое время.

        tr_day_5 = CreateData.tr_day_for_group(self.gr_5_mp_al)
        tr_day_5.pay_visitors.add(self.player_6)

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_5)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_5
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_5)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_5
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_5)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_5
        )

        (
            player_text,
            player_markup,
            admin_text,
            admin_markup,
        ) = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_5)
        self.assert_no_places_choose_another(
            player_text, player_markup, admin_text, admin_markup, tr_day_5
        )

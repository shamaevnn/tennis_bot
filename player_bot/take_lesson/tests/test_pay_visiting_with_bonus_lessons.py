from django.test import TestCase
from base.utils.for_tests import CreateData
from player_bot.take_lesson.group.manage_data import PAYMENT_MONEY_AND_BONUS_LESSONS
from player_bot.take_lesson.group.utils import (
    handle_choosing_type_of_payment_for_pay_visiting_when_have_bonus_lessons,
)
from tennis_bot.settings import TARIF_PAYMENT_ADD_LESSON


class Tests(TestCase):
    def setUp(self):
        self.group_player_with_bonus_lessons = CreateData.group_player(
            tg_id=123, first_name="Nikita 1", bonus_lesson=10
        )

        self.player_1 = CreateData.group_player(tg_id=1, first_name="player_1")
        self.player_2 = CreateData.group_player(tg_id=2, first_name="player_2")
        self.player_3 = CreateData.group_player(tg_id=3, first_name="player_3")
        self.player_4 = CreateData.group_player(tg_id=4, first_name="player_4")

        self.group_4_max_players = CreateData.group(max_players=4)
        self.group_4_max_players.players.add(
            self.player_1, self.player_2, self.player_3, self.player_4
        )

    def test_payment_money_and_bonus_lesson(self):
        tr_day_4 = CreateData.tr_day_for_group(self.group_4_max_players)
        tr_day_4.absent.add(self.player_4)

        # если записался за счёт платных отыгрышей, то убавляется отыгрыш и добавляешься в pay_bonus_visitors
        current_bonus_lessons = self.group_player_with_bonus_lessons.bonus_lesson
        (
            player_text,
            admin_text,
        ) = handle_choosing_type_of_payment_for_pay_visiting_when_have_bonus_lessons(
            self.group_player_with_bonus_lessons,
            tr_day_4,
            PAYMENT_MONEY_AND_BONUS_LESSONS,
        )
        self.assertIn(
            f"Не забудь заплатить <b>{TARIF_PAYMENT_ADD_LESSON}₽</b>", player_text
        )
        self.assertIn(
            f"b>за счёт платных отыгрышей, не забудь взять {TARIF_PAYMENT_ADD_LESSON}₽.</b>",
            admin_text,
        )

        self.assertIn(
            self.group_player_with_bonus_lessons, tr_day_4.pay_bonus_visitors.all()
        )
        self.assertEqual(
            self.group_player_with_bonus_lessons.bonus_lesson, current_bonus_lessons - 1
        )

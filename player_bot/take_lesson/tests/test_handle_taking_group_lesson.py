from datetime import datetime, timedelta, time

from django.test import TestCase

from base.models import Player, TrainingGroup, GroupTrainingDay
from player_bot.take_lesson.static_text import NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER, CHOOSE_TYPE_OF_PAYMENT
from player_bot.take_lesson.group.keyboards import choose_type_of_payment_for_group_lesson_keyboard, \
    back_to_group_times_when_no_left_keyboard
from player_bot.take_lesson.group.utils import handle_taking_group_lesson
from tennis_bot.settings import TARIF_PAYMENT_ADD_LESSON, TARIF_GROUP, TARIF_ARBITRARY


def create_group_player(id: int, first_name: str, **kwargs):
    player = Player.objects.create(tg_id=id, first_name=first_name, last_name=first_name, status=Player.STATUS_TRAINING, **kwargs)
    return player


def create_arbitrary_player(id: int, first_name: str, **kwargs):
    player = Player.objects.create(tg_id=id, first_name=first_name, last_name=first_name, status=Player.STATUS_ARBITRARY, **kwargs)
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


class NoFreePlacesTests(TestCase):
    def assert_no_places_choose_another(self, player_text, player_markup, admin_text, admin_markup, tr_day):
        self.assertEqual(player_text, NO_PLACES_FOR_THIS_TIME_CHOOSE_ANOTHER)
        self.assertEqual(
            player_markup, back_to_group_times_when_no_left_keyboard(
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
        self.gr_u_w_bl = create_group_player(id=350490234, first_name='Nikita 1', bonus_lesson=10)
        self.gr_u_wo_bl = create_group_player(id=350490235, first_name='Nikita 2', bonus_lesson=0)
        self.arb_u_w_bl = create_arbitrary_player(id=350490236, first_name='Nikita 3', bonus_lesson=10)
        self.arb_u_wo_bl = create_arbitrary_player(id=350490236, first_name='Nikita 4', bonus_lesson=0)

        self.player_1 = create_group_player(id=1, first_name='player_1')
        self.player_2 = create_group_player(id=2, first_name='player_2')
        self.player_3 = create_group_player(id=3, first_name='player_3')
        self.player_4 = create_group_player(id=4, first_name='player_4')
        self.player_5 = create_group_player(id=5, first_name='player_5')
        self.player_6 = create_group_player(id=6, first_name='player_6')
        self.player_7 = create_group_player(id=7, first_name='player_7')
        self.player_8 = create_group_player(id=8, first_name='player_8')
        self.player_9 = create_group_player(id=9, first_name='player_9')

        self.gr_4_mp = create_group(max_players=4)
        self.gr_6_mp = create_group(max_players=6)
        self.gr_4_mp.players.add(self.player_1, self.player_2, self.player_3, self.player_4)
        self.gr_6_mp.players.add(self.player_1, self.player_2, self.player_3, self.player_4, self.player_5, self.player_6)

        self.gr_4_mp_al = create_group(max_players=4, available_for_additional_lessons=True)
        self.gr_5_mp_al = create_group(max_players=5, available_for_additional_lessons=True)
        self.gr_6_mp_al = create_group(max_players=6, available_for_additional_lessons=True)
        self.gr_4_mp_al.players.add(self.player_1, self.player_2, self.player_3, self.player_4)
        self.gr_5_mp_al.players.add(self.player_1, self.player_2, self.player_3, self.player_4, self.player_5)
        self.gr_6_mp_al.players.add(self.player_1, self.player_2, self.player_3, self.player_4, self.player_5, self.player_6)

    def test_no_free_places_no_additional_lessons(self):
        tr_day_4 = create_tr_day_for_group(self.gr_4_mp)
        tr_day_6 = create_tr_day_for_group(self.gr_6_mp)

        # все игроки из группы придут на занятие и нельзя записаться на доп. места
        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_4)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_4)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_4)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_4)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_4)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_4)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_4)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_4)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_6)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_6)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_6)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_6)

    def test_no_free_places_with_all_kinds_of_visitors_and_available_additional_lessons(self):
        tr_day_4 = create_tr_day_for_group(self.gr_4_mp_al)
        tr_day_4.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_4.visitors.add(self.player_5)
        tr_day_4.pay_visitors.add(self.player_6)
        tr_day_4.pay_bonus_visitors.add(self.player_7)

        tr_day_6 = create_tr_day_for_group(self.gr_6_mp_al)
        tr_day_6.absent.add(self.player_1, self.player_2, self.player_3)
        tr_day_6.visitors.add(self.player_7)
        tr_day_6.pay_visitors.add(self.player_8)
        tr_day_6.pay_bonus_visitors.add(self.player_9)

        # если есть отыгрыши, то должна появиться следующая клава с выбором типа оплаты:
        # за отыгрыш + деньги либо просто за деньги
        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_4)
        self.assertEqual(player_text, CHOOSE_TYPE_OF_PAYMENT)
        self.assertEqual(
            player_markup, choose_type_of_payment_for_group_lesson_keyboard(
                    payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                    tr_day_id=tr_day_4.id,
                    tarif=TARIF_GROUP,
            )
        )
        self.assertEqual(admin_text, '')
        self.assertIsNone(admin_markup)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_4)
        self.assertEqual(player_text, CHOOSE_TYPE_OF_PAYMENT)
        self.assertEqual(
            player_markup, choose_type_of_payment_for_group_lesson_keyboard(
                payment_add_lesson=TARIF_PAYMENT_ADD_LESSON,
                tr_day_id=tr_day_4.id,
                tarif=TARIF_ARBITRARY,
            )
        )
        self.assertEqual(admin_text, '')
        self.assertIsNone(admin_markup)

        # если нет отыгрышей, то добавляем пользователя в pay_visitors и соответствующие texts
        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_4)
        self.assertIn(f"Не забудь заплатить <b>{TARIF_GROUP}₽</b>", player_text)
        self.assertIn(f"<b>не за счет отыгрышей, не забудь взять {TARIF_GROUP}₽.</b>", admin_text)
        self.assertIsNone(player_markup)
        self.assertIsNone(admin_markup)
        self.assertIn(self.gr_u_wo_bl, tr_day_4.pay_visitors.all())

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_4)
        self.assertIn(f"Не забудь заплатить <b>{TARIF_ARBITRARY}₽</b>", player_text)
        self.assertIn(f"<b>не за счет отыгрышей, не забудь взять {TARIF_ARBITRARY}₽.</b>", admin_text)
        self.assertIsNone(player_markup)
        self.assertIsNone(admin_markup)
        self.assertIn(self.arb_u_wo_bl, tr_day_4.pay_visitors.all())

        # если максимум 6 игроков и все места заняты, то нужно предлагать другое время
        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_6)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_6)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_6)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_6)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_6)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_6)

    def test_full_group_one_pay_plus_one(self):
        # additional_lessons=True, группа из 5 человек, один записался за деньги,
        # второй хочет записаться за платные отыгрыши, не можем записать, т.к. максимум 6 человек на занятии.
        # надо предлагать другое время.

        tr_day_5 = create_tr_day_for_group(self.gr_5_mp_al)
        tr_day_5.pay_visitors.add(self.player_6)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_w_bl, tr_day_5)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_5)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.arb_u_wo_bl, tr_day_5)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_5)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_wo_bl, tr_day_5)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_5)

        player_text, player_markup, admin_text, admin_markup = handle_taking_group_lesson(self.gr_u_w_bl, tr_day_5)
        self.assert_no_places_choose_another(player_text, player_markup, admin_text, admin_markup, tr_day_5)

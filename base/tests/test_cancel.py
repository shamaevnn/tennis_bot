from django.test import TestCase
from base.models import GroupTrainingDay, Cancel
from base.utils.for_tests import CreateData
from base.utils import change_available_status


class CancelLessonCase(TestCase):
    def test_cancel_lesson_for_visitor(self) -> None:
        # если ученик записался на занятие в счёт отыгрыша, то "отмена" не начисляется, а возвращается 1 "отыгрыш".
        player = CreateData.group_player(tg_id=350490234, first_name="Nikita")

        group = CreateData.group()
        group.players.add(player)
        trday = CreateData.tr_day_for_group(group)
        trday.visitors.add(player)

        trday.available_status = GroupTrainingDay.AVAILABLE
        trday.save()
        visitor_bonus_lessons_before = player.bonus_lesson
        change_available_status.change_tr_day_available_status_and_send_alert(
            trday, GroupTrainingDay.CANCELLED
        )

        visitor = trday.visitors.first()
        self.assertEqual(visitor.bonus_lesson, visitor_bonus_lessons_before + 1)

    def test_not_available_lesson(self) -> None:
        # если занятие не доступно то всем начисляется 1 отыгрышь
        player = CreateData.group_player(tg_id=350490234, first_name="Nikita")

        group = CreateData.group()
        group.players.add(player)
        trday = CreateData.tr_day_for_group(group)
        trday.visitors.add(player)

        trday.available_status = GroupTrainingDay.AVAILABLE
        trday.save()
        visitor_bonus_lessons_before = player.bonus_lesson
        change_available_status.change_tr_day_available_status_and_send_alert(
            trday, GroupTrainingDay.NOT_AVAILABLE
        )

        visitor = trday.visitors.first()
        self.assertEqual(visitor.bonus_lesson, visitor_bonus_lessons_before + 1)

    def test_cancel_lesson_for_pay_visitor(self) -> None:
        # если у ученика занятие по расписанию группы, то ему начисляется в личный кабинет одна "отмена".
        player = CreateData.group_player(tg_id=350490234, first_name="Nikita")

        group = CreateData.group()
        group.players.add(player)
        trday = CreateData.tr_day_for_group(group)

        trday.pay_visitors.add(player)
        trday.available_status = GroupTrainingDay.AVAILABLE
        trday.save()

        pay_visitor_cancelled_lesson_before = 0

        pay_visitor_cancelled_lesson_after = 0

        cancel = Cancel.get_cancel_from_player(player, trday.date)

        if cancel is not None:
            pay_visitor_cancelled_lessons_before = cancel.n_cancelled_lessons

        change_available_status.change_tr_day_available_status_and_send_alert(
            trday, GroupTrainingDay.CANCELLED
        )

        cancel = Cancel.get_cancel_from_player(player, trday.date)
        pay_visitor_cancelled_lesson_after = cancel.n_cancelled_lessons

        self.assertEqual(
            pay_visitor_cancelled_lesson_before + 1, pay_visitor_cancelled_lesson_after
        )

    def test_cancel_lesson_for_pay_bonus_visitors(self) -> None:
        # У игрока 0 отыгрышей и он записался на занятие за отыгрыш:
        # в случае "отмены" занятия: ни отмена, ни отыгрыш не добавляется.
        player = CreateData.group_player(tg_id=350490234, first_name="Nikita")

        group = CreateData.group()
        group.players.add(player)
        trday = CreateData.tr_day_for_group(group)
        trday.pay_bonus_visitors.add(player)

        trday.available_status = GroupTrainingDay.AVAILABLE
        trday.save()

        pay_visitor_bonus_lessons_before = player.bonus_lesson

        pay_visitor_cancelled_lesson_before = 0

        pay_visitor_cancelled_lesson_after = 0

        cancel = Cancel.get_cancel_from_player(player, trday.date)

        if cancel is not None:
            pay_visitor_cancelled_lesson_before = cancel.n_cancelled_lessons

        change_available_status.change_tr_day_available_status_and_send_alert(
            trday, GroupTrainingDay.CANCELLED
        )

        cancel = Cancel.get_cancel_from_player(player, trday.date)
        if cancel is not None:
            pay_visitor_cancelled_lesson_after = cancel.n_cancelled_lessons

        pay_visitor = trday.pay_bonus_visitors.first()

        self.assertEqual(
            pay_visitor_cancelled_lesson_before, pay_visitor_cancelled_lesson_after
        )
        self.assertEqual(pay_visitor.bonus_lesson, pay_visitor_bonus_lessons_before)

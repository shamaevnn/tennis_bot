from django.test import TestCase

from admin_bot.send_message.manage_data import (
    ALL_GROUPS,
    SEND_TO_ALL,
    SEND_TO_ARBITRARY_SCHEDULE,
)
from admin_bot.send_message.static_text import (
    SENDING_TO_ALL_GROUPS_TYPE_TEXT,
    WILL_SEND_TO_ALL_TYPE_TEXT,
    WILL_SEND_TO_FREE_SCHEDULE,
)
from admin_bot.send_message.utils import get_text_and_player_ids_to_send_message_to
from base.utils.for_tests import CreateData


class TestCases(TestCase):
    def setUp(self) -> None:
        self.waiting_player = CreateData.waiting_player(1)
        self.finished_player = CreateData.finished_player(2)
        self.arbitrary_player = CreateData.arbitrary_player(3)

        self.group_player = CreateData.group_player(4)
        self.group = CreateData.group()
        self.group.players.add(self.group_player)

        self.group_player_2 = CreateData.group_player(5)
        self.group_2 = CreateData.group()
        self.group_2.players.add(self.group_player_2)

        self.ind_group = CreateData.ind_group(self.arbitrary_player)
        self.rent_group = CreateData.rent_group(self.arbitrary_player)

    def test_send_to_all_groups(self):
        # отправляем только группам (бандам), но не индивидуальные и не для аренды
        text, player_ids = get_text_and_player_ids_to_send_message_to(
            group_ids=[ALL_GROUPS]
        )

        self.assertEqual(text, SENDING_TO_ALL_GROUPS_TYPE_TEXT)

        self.assertIn(self.group_player.tg_id, player_ids)
        self.assertIn(self.group_player_2.tg_id, player_ids)
        self.assertNotIn(self.waiting_player.tg_id, player_ids)
        self.assertNotIn(self.arbitrary_player.tg_id, player_ids)
        self.assertNotIn(self.finished_player.tg_id, player_ids)

        self.assertEqual(2, len(player_ids))

    def test_send_to_all(self):
        # отправляем вообще всем игрокам
        text, player_ids = get_text_and_player_ids_to_send_message_to(
            group_ids=[SEND_TO_ALL]
        )

        self.assertEqual(text, WILL_SEND_TO_ALL_TYPE_TEXT)

        self.assertIn(self.arbitrary_player.tg_id, player_ids)
        self.assertIn(self.group_player.tg_id, player_ids)
        self.assertIn(self.group_player_2.tg_id, player_ids)
        self.assertNotIn(self.waiting_player.tg_id, player_ids)
        self.assertNotIn(self.finished_player.tg_id, player_ids)

        self.assertEqual(3, len(player_ids))

    def test_send_to_arbitrary_schedule(self):
        # отправляем только тем, кто ходит по свободному графику
        text, player_ids = get_text_and_player_ids_to_send_message_to(
            group_ids=[SEND_TO_ARBITRARY_SCHEDULE]
        )

        self.assertEqual(text, WILL_SEND_TO_FREE_SCHEDULE)

        self.assertIn(self.arbitrary_player.tg_id, player_ids)
        self.assertNotIn(self.group_player.tg_id, player_ids)
        self.assertNotIn(self.group_player_2.tg_id, player_ids)
        self.assertNotIn(self.waiting_player.tg_id, player_ids)
        self.assertNotIn(self.finished_player.tg_id, player_ids)

        self.assertEqual(1, len(player_ids))

    def test_send_to_chosen_groups(self):
        text, player_ids = get_text_and_player_ids_to_send_message_to(
            group_ids=[self.group.id]
        )

        self.assertIn(self.group.name, text)

        self.assertIn(self.group_player.tg_id, player_ids)
        self.assertNotIn(self.group_player_2.tg_id, player_ids)
        self.assertNotIn(self.waiting_player.tg_id, player_ids)
        self.assertNotIn(self.arbitrary_player.tg_id, player_ids)
        self.assertNotIn(self.finished_player.tg_id, player_ids)

        self.assertEqual(1, len(player_ids))

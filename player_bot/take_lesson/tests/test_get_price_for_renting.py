from django.test import TestCase

from player_bot.take_lesson.rent.utils import _get_price_for_renting


class TestPriceForRenting(TestCase):
    def test_get_price(self):
        # 2 игрока
        self.assertEqual(700, _get_price_for_renting(2, 1))
        self.assertEqual(1050, _get_price_for_renting(2, 1.5))
        self.assertEqual(1400, _get_price_for_renting(2, 2))

        # 3 игрока
        self.assertEqual(800, _get_price_for_renting(3, 1))
        self.assertEqual(1200, _get_price_for_renting(3, 1.5))
        self.assertEqual(1600, _get_price_for_renting(3, 2))

        # 4 игрока
        self.assertEqual(900, _get_price_for_renting(4, 1))
        self.assertEqual(1350, _get_price_for_renting(4, 1.5))
        self.assertEqual(1800, _get_price_for_renting(4, 2))

        # 5 игроков
        self.assertEqual(1000, _get_price_for_renting(5, 1))
        self.assertEqual(1500, _get_price_for_renting(5, 1.5))
        self.assertEqual(2000, _get_price_for_renting(5, 2))

        # 6 игроков
        self.assertEqual(1100, _get_price_for_renting(6, 1))
        self.assertEqual(1650, _get_price_for_renting(6, 1.5))
        self.assertEqual(2200, _get_price_for_renting(6, 2))

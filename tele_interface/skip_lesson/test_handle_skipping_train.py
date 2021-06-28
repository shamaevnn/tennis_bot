from django.test import TestCase

from tele_interface.take_lesson.test_get_potential_days_for_group_training import create_group_user


class AvailableForAdditionalLessonsTestCases(TestCase):
    def setUp(self):
        self.me = create_group_user(id=1, first_name='Nikita')

    def tes
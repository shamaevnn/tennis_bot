from django.test import TestCase

from base.redis.base import BaseRedis


class RedisClientsTestCases(TestCase):
    def test_all_subclasses_of_base_redis_have_unique_name(self):
        all_names = []
        for subclass in BaseRedis.__subclasses__():
            all_names.append(subclass.name)
        self.assertEqual(len(all_names), len(set(all_names)))

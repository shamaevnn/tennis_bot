from typing import Optional, List, Union

from base.redis.base import BaseRedis

from django.core.cache import cache


class SentTrDaysAlerts(BaseRedis):
    name = "sent_tr_day_alerts"

    @classmethod
    def _get_key_name(cls, tr_day_id: Union[str, int], player_id: str) -> str:
        if getattr(cls, "name") is None:
            raise ValueError(f"Define name attribute in {cls.__name__}")
        return f"{cls.name}_{tr_day_id}_{player_id}"

    @classmethod
    def get(cls, tr_day_id: int, player_id: str) -> Optional[bool]:
        key = cls._get_key_name(tr_day_id, player_id)
        res = cache.get(key)
        return res

    @classmethod
    def put(cls, tr_day_id: int, player_id: str) -> None:
        seconds_in_24_hours = 60 * 60 * 24
        res = cls.get(tr_day_id, player_id)
        if res is None:
            key = cls._get_key_name(tr_day_id, player_id)
            cache.set(key, True, timeout=seconds_in_24_hours)

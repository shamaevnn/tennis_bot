import random
import string
from datetime import datetime, timedelta, time
from typing import Optional

from base.models import Player, TrainingGroup, GroupTrainingDay


class CreateData:
    @classmethod
    def _get_random_string(cls, length: int) -> str:
        return "".join(random.choices(string.ascii_letters, k=length))

    @classmethod
    def player(cls, tg_id: int, first_name: Optional[str] = None, **kwargs) -> Player:
        if first_name is None:
            first_name = cls._get_random_string(length=10)

        player = Player.objects.create(tg_id=tg_id, first_name=first_name, **kwargs)
        return player

    @classmethod
    def group_player(
        cls, tg_id: int, first_name: Optional[str] = None, **kwargs
    ) -> Player:
        return cls.player(
            tg_id=tg_id, first_name=first_name, status=Player.STATUS_TRAINING, **kwargs
        )

    @classmethod
    def arbitrary_player(
        cls, tg_id: int, first_name: Optional[str] = None, **kwargs
    ) -> Player:
        return cls.player(
            tg_id=tg_id, first_name=first_name, status=Player.STATUS_ARBITRARY, **kwargs
        )

    @classmethod
    def finished_player(
        cls, tg_id: int, first_name: Optional[str] = None, **kwargs
    ) -> Player:
        return cls.player(
            tg_id=tg_id, first_name=first_name, status=Player.STATUS_FINISHED, **kwargs
        )

    @classmethod
    def waiting_player(
        cls, tg_id: int, first_name: Optional[str] = None, **kwargs
    ) -> Player:
        return cls.player(
            tg_id=tg_id, first_name=first_name, status=Player.STATUS_WAITING, **kwargs
        )

    @classmethod
    def group(
        cls,
        name: Optional[str] = None,
        max_players=6,
        status=TrainingGroup.STATUS_GROUP,
        level=TrainingGroup.LEVEL_GREEN,
        **kwargs
    ) -> TrainingGroup:
        if name is None:
            name = cls._get_random_string(length=10)
        group = TrainingGroup.objects.create(
            name=name, max_players=max_players, status=status, level=level, **kwargs
        )
        return group

    @classmethod
    def rent_group(cls, player: Player) -> TrainingGroup:
        return TrainingGroup.get_or_create_rent_group(player=player)

    @classmethod
    def ind_group(cls, player: Player) -> TrainingGroup:
        return TrainingGroup.get_or_create_ind_group(player=player)

    @classmethod
    def tr_day_for_group(
        cls, group, date=None, start_time=None, **kwargs
    ) -> GroupTrainingDay:
        if date is None:
            today = datetime.today()
            date = (today + timedelta(days=2)).date()
        if start_time is None:
            start_time = time(9, 30)

        tr_day = GroupTrainingDay.objects.create(
            group=group, date=date, start_time=start_time, **kwargs
        )
        return tr_day

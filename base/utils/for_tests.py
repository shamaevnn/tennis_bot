from datetime import datetime, timedelta, time

from base.models import Player, TrainingGroup, GroupTrainingDay


class CreateData:
    @classmethod
    def group_player(cls, tg_id: int, first_name: str, **kwargs) -> Player:
        player = Player.objects.create(
            tg_id=tg_id, first_name=first_name, status=Player.STATUS_TRAINING, **kwargs
        )
        return player

    @classmethod
    def arbitrary_player(cls, tg_id: int, first_name: str, **kwargs) -> Player:
        player = Player.objects.create(
            tg_id=tg_id, first_name=first_name, status=Player.STATUS_ARBITRARY, **kwargs
        )
        return player

    @classmethod
    def group(
        cls,
        name="БАНДА №1",
        max_players=6,
        status=TrainingGroup.STATUS_GROUP,
        level=TrainingGroup.LEVEL_GREEN,
        **kwargs
    ) -> TrainingGroup:
        group = TrainingGroup.objects.create(
            name=name, max_players=max_players, status=status, level=level, **kwargs
        )
        return group

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

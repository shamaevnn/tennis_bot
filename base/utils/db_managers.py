from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Manager


class ModelwithTimeManager(models.Manager):
    def available_adult_train(self, *args, **kwargs):
        from base.models import GroupTrainingDay

        return self.filter(
            available_status = GroupTrainingDay.AVAILABLE,
            status = GroupTrainingDay.GROUP_ADULT_TRAIN,
            is_deleted=False,
            *args,
            **kwargs
        )


class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class CoachPlayerManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_coach=True)

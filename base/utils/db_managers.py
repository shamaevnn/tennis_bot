from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import Manager


class ModelwithTimeManager(models.Manager):
    def tr_day_is_my_available(self, *args, **kwargs):
        from base.models import GroupTrainingDay
        return self.filter(is_available=True, tr_day_status=GroupTrainingDay.MY_TRAIN_STATUS, *args, **kwargs)


class GetOrNoneManager(models.Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class CoachPlayerManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_coach=True)

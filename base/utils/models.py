from django.db import models
from django.utils import timezone

from base.utils.db_managers import ModelwithTimeManager


nb = dict(null=True, blank=True)


class ModelwithTime(models.Model):
    dttm_added = models.DateTimeField(default=timezone.now)
    dttm_deleted = models.DateTimeField(null=True, blank=True)

    objects = ModelwithTimeManager()

    class Meta:
        abstract = True


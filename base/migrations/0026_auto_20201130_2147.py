# Generated by Django 2.0.5 on 2020-11-30 21:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0025_auto_20201130_1040'),
    ]

    operations = [
        migrations.AddField(
            model_name='traininggroup',
            name='tarif_for_one_lesson',
            field=models.PositiveIntegerField(default=400, verbose_name='Тариф за одно занятие'),
        ),
        migrations.AlterField(
            model_name='alertslog',
            name='dttm_sent',
            field=models.DateTimeField(default=datetime.datetime(2020, 12, 1, 0, 47, 9, 821531)),
        ),
    ]

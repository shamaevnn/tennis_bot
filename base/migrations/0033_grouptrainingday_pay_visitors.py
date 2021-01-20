# Generated by Django 2.0.5 on 2021-01-20 20:08

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_traininggroup_available_for_additional_lessons'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouptrainingday',
            name='pay_visitors',
            field=models.ManyToManyField(blank=True, help_text='Заплатили за занятие', related_name='pay_visitors', to=settings.AUTH_USER_MODEL, verbose_name='Заплатившие игроки'),
        ),
    ]

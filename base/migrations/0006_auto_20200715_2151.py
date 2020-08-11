# Generated by Django 2.0.5 on 2020-07-15 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='time_before_cancel',
            field=models.DurationField(help_text='H:M:S', null=True),
        ),
        migrations.AlterField(
            model_name='grouptrainingday',
            name='duration',
            field=models.DurationField(blank=True, help_text='H:M:S', null=True,
                                       verbose_name='Продолжительность занятия'),
        ),
    ]

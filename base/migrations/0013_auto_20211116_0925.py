# Generated by Django 3.2.4 on 2021-11-16 06:25

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0012_from_users_to_players'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='player',
            managers=[
                ('coaches', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='player',
            name='is_coach',
            field=models.BooleanField(default=False, verbose_name='Тренер'),
        ),
        migrations.AlterField(
            model_name='grouptrainingday',
            name='is_available',
            field=models.BooleanField(default=True, help_text='Будет ли в этот день тренировка у этой группы', verbose_name='Доступно'),
        ),
        migrations.AlterField(
            model_name='player',
            name='tg_id',
            field=models.PositiveBigIntegerField(blank=True, null=True, verbose_name='telegram id'),
        ),
        migrations.AlterField(
            model_name='traininggroup',
            name='max_players',
            field=models.SmallIntegerField(default=6, verbose_name='Макс. игроков'),
        ),
    ]
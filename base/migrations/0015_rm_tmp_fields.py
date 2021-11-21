# Generated by Django 3.2.4 on 2021-11-15 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0014_tr_day_players'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alertslog',
            name='player',
        ),
        migrations.RemoveField(
            model_name='grouptrainingday',
            name='absent',
        ),
        migrations.RemoveField(
            model_name='grouptrainingday',
            name='pay_bonus_visitors',
        ),
        migrations.RemoveField(
            model_name='grouptrainingday',
            name='pay_visitors',
        ),
        migrations.RemoveField(
            model_name='grouptrainingday',
            name='visitors',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='player',
        ),
        migrations.RemoveField(
            model_name='traininggroup',
            name='users',
        ),
        migrations.RenameField(
            model_name='alertslog',
            old_name='player_tmp',
            new_name='player',
        ),
        migrations.RenameField(
            model_name='grouptrainingday',
            old_name='players_absent',
            new_name='absent',
        ),
        migrations.RenameField(
            model_name='grouptrainingday',
            old_name='players_pay_bonus_visitors',
            new_name='pay_bonus_visitors',
        ),
        migrations.RenameField(
            model_name='grouptrainingday',
            old_name='players_pay_visitors',
            new_name='pay_visitors',
        ),
        migrations.RenameField(
            model_name='grouptrainingday',
            old_name='players_visitors',
            new_name='visitors',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='player_tmp',
            new_name='player',
        ),
        migrations.AlterField(
            model_name='traininggroup',
            name='players',
            field=models.ManyToManyField(to='base.Player', verbose_name='Игроки группы'),
        ),
    ]

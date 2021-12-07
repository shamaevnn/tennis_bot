# Generated by Django 3.2.9 on 2021-11-26 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0018_player_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='status',
            field=models.CharField(choices=[('W', 'в ожидании'), ('G', 'групповые тренировки'), ('A', 'свободный график'), ('F', 'закончил'), ('P', 'родитель')], default='W', max_length=1, verbose_name='статус'),
        ),
    ]
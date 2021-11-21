# Generated by Django 3.2.4 on 2021-11-20 13:54

from django.db import migrations


def insert_players(apps, schema_editor):
    User = apps.get_model('base', 'User')
    Player = apps.get_model('base', 'Player')

    for user in User.objects.all():
        Player.objects.create(
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            tg_id=user.id,
            tg_username=user.telegram_username,
            has_blocked_bot=user.is_blocked,
            status=user.status,
            time_before_cancel=user.time_before_cancel,
            bonus_lesson=user.bonus_lesson,
        )


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_create_player_model'),
    ]

    operations = [
        migrations.RunPython(insert_players),
    ]

# Generated by Django 3.2.4 on 2021-11-15 22:16

from django.db import migrations, models
import django.db.models.deletion


def insert_data_from_users_to_players(apps, schema_editor):
    Player = apps.get_model("base", "Player")
    AlertsLog = apps.get_model("base", "AlertsLog")

    for alert_log in AlertsLog.objects.filter(player__isnull=False).iterator():
        player_tmp = Player.objects.filter(tg_id=alert_log.player.id).first()
        alert_log.player_tmp = player_tmp
        alert_log.save()


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0011_insert_players_to_groups"),
    ]

    operations = [
        migrations.AddField(
            model_name="alertslog",
            name="player_tmp",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="base.player",
            ),
        ),
        migrations.RunPython(insert_data_from_users_to_players),
    ]

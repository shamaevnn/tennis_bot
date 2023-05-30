# Generated by Django 3.2.12 on 2023-05-25 13:46

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils import timezone

from base.models import PlayerCancelLesson


def create_сancels(apps, schema_editor):
    player_model = apps.get_model("base", "Player")
    for player in player_model.objects.All():
        PlayerCancelLesson.add_cancel(player, timezone.now())


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0025_auto_20230525_1455"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerCancelLesson",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "n_cancelled_lessons",
                    models.SmallIntegerField(
                        default=0, verbose_name="Количество отмен"
                    ),
                ),
                (
                    "date",
                    models.DateField(
                        default=django.utils.timezone.now, verbose_name="Дата"
                    ),
                ),
                (
                    "player",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="base.player",
                        verbose_name="Игрок",
                    ),
                ),
            ],
        ),
        migrations.RunPython(create_сancels),
        migrations.RemoveField(
            model_name="player",
            name="n_cancelled_lessons",
        ),
    ]

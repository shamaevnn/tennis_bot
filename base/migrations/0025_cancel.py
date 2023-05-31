# Generated by Django 3.2.12 on 2023-05-25 13:46
from datetime import date

from django.db import migrations, models
import django.utils.timezone


def create_cancels(apps, schema_editor):
    player_model = apps.get_model("base", "Player")
    player_cancel_lesson_model = apps.get_model("base", "PlayerCancelLesson")

    date_with_first_day = date.today().replace(day=1)

    for player in player_model.objects.all():
        cancel_for_player = player_cancel_lesson_model(
            player=player,
            n_cancelled_lessons=player.n_cancelled_lessons,
            date=date_with_first_day,
        )
        cancel_for_player.save()


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0024_auto_20230507_2205"),
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
        migrations.RunPython(create_cancels),
        migrations.RemoveField(
            model_name="player",
            name="n_cancelled_lessons",
        ),
    ]

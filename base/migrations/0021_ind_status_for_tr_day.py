# Generated by Django 3.1.7 on 2022-01-08 11:37

from django.db import migrations, models


def update_tr_day_status_for_tr_days(apps, schema_editor):
    GroupTrainingDay = apps.get_model("base", "GroupTrainingDay")

    GroupTrainingDay.objects.filter(is_individual=True).update(status="I")


class Migration(migrations.Migration):

    dependencies = [
        ("base", "0020_alter_payment_year"),
    ]

    operations = [
        migrations.AlterField(
            model_name="grouptrainingday",
            name="tr_day_status",
            field=models.CharField(
                choices=[
                    ("M", "групповая тренировка для взрослых"),
                    ("I", "индивидуальная тренировка"),
                    ("R", "аренда корта"),
                ],
                default="M",
                help_text="Моя тренировка или аренда",
                max_length=1,
                verbose_name="Статус",
            ),
        ),
        migrations.RenameField(
            model_name="grouptrainingday",
            old_name="tr_day_status",
            new_name="status",
        ),
        migrations.RunPython(update_tr_day_status_for_tr_days),
        migrations.RemoveField(
            model_name="grouptrainingday",
            name="is_individual",
        ),
    ]
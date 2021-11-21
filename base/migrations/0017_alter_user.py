# Generated by Django 3.2.4 on 2021-11-21 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0016_rm_users_except_admins'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.RemoveField(
            model_name='user',
            name='add_info',
        ),
        migrations.RemoveField(
            model_name='user',
            name='bonus_lesson',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_blocked',
        ),
        migrations.RemoveField(
            model_name='user',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='user',
            name='status',
        ),
        migrations.RemoveField(
            model_name='user',
            name='telegram_username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='time_before_cancel',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False,
                                      help_text='Designates that this user has all permissions without explicitly assigning them.',
                                      verbose_name='superuser status'),
        ),
        migrations.AlterField(
            model_name='player',
            name='bonus_lesson',
            field=models.SmallIntegerField(default=0, verbose_name='Количество отыгрышей'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Имя'),
        ),
    ]
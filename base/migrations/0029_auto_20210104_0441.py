# Generated by Django 2.0.5 on 2021-01-04 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0028_auto_20210104_0441'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alertslog',
            name='dttm_sent',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]

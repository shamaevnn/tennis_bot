# Generated by Django 2.0.5 on 2020-07-14 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_auto_20200714_2043'),
    ]

    operations = [
        migrations.RenameField(
            model_name='traininggroup',
            old_name='user',
            new_name='users',
        ),
    ]

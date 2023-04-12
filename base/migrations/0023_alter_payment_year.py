# Generated by Django 3.2.12 on 2022-12-17 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_grouptrainingday_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='year',
            field=models.CharField(choices=[('0', '2020'), ('1', '2021'), ('2', '2022'), ('3', '2023')], max_length=1, verbose_name='год'),
        ),
    ]
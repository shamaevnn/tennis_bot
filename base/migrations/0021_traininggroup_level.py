# Generated by Django 2.0.5 on 2020-09-04 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_auto_20200904_1432'),
    ]

    operations = [
        migrations.AddField(
            model_name='traininggroup',
            name='level',
            field=models.CharField(choices=[('G', '\U0001f7e2мяч\U0001f7e2'), ('O', '\U0001f7e0мяч\U0001f7e0')], default='O', max_length=1, verbose_name='Уровень группы'),
        ),
    ]
# Generated by Django 3.2.4 on 2021-11-20 14:56

from django.db import migrations


def rm_non_admin_users(apps, schema_editor):
    User = apps.get_model('base', 'User')
    User.objects.exclude(is_superuser=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_rm_tmp_fields'),
    ]

    operations = [
        migrations.RunPython(rm_non_admin_users),
    ]

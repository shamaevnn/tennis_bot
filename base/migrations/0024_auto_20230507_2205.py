# Generated by Django 3.2.12 on 2023-05-07 19:05

from django.db import migrations, models

def set_avialable_state(apps, schema_editor):
    model = apps.get_model('base','grouptrainingday')
    model.objects.filter(is_available=False).update(available_status='N')
       
class Migration(migrations.Migration):

    dependencies = [
        ('base', '0023_alter_payment_year'),
    ]

    operations = [
        migrations.AddField(
            model_name='grouptrainingday',
            name='available_status',
            field=models.CharField(choices=[('A', 'доступно'), ('N', 'недоступно'), ('C', 'отменено')], default='A', help_text='Статус занятия', max_length=1, verbose_name='Статус занятия'),
        ),
        migrations.AddField(
            model_name='player',
            name='n_cancelled_lessons',
            field=models.SmallIntegerField(default=0, verbose_name='Количество отмен'),
        ),
        migrations.RunPython(set_avialable_state),
        migrations.RunSQL("ALTER TABLE base_grouptrainingday DROP COLUMN is_available")
        
    ]

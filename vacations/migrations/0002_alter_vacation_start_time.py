# Generated by Django 3.2.9 on 2022-02-12 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacations', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacation',
            name='start_time',
            field=models.TimeField(default='07:45:00', verbose_name='Heure début'),
        ),
    ]

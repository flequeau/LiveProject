# Generated by Django 3.2.9 on 2021-12-10 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repartition', '0003_auto_20211210_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='operator',
            name='forname',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='operator',
            name='speciality',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
# Generated by Django 3.2.9 on 2022-02-20 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subdivision', '0004_compta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='compta',
            name='gerant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gerant', to='subdivision.are', verbose_name='Gerant'),
        ),
    ]

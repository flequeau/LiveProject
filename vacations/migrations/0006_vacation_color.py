# Generated by Django 3.2.9 on 2022-02-17 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vacations', '0005_alter_vacataire_color'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacation',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='Couleur', to='vacations.vacataire'),
        ),
    ]

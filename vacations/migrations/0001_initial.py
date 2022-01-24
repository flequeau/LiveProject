# Generated by Django 3.2.9 on 2022-01-24 20:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('subdivision', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacataire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nom')),
                ('forname', models.CharField(max_length=50, verbose_name='Prénom')),
                ('adress1', models.CharField(blank=True, max_length=50, null=True, verbose_name='Adresse')),
                ('adress2', models.CharField(blank=True, max_length=50, null=True, verbose_name="Complément d'adresse")),
                ('town', models.CharField(blank=True, max_length=50, null=True, verbose_name='Ville')),
                ('postalcode', models.CharField(blank=True, max_length=10, null=True, verbose_name='Code postal')),
                ('telmob', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tél. Mobile')),
                ('tel2', models.CharField(blank=True, max_length=20, null=True, verbose_name='Tél. Perso')),
                ('email', models.EmailField(blank=True, max_length=50, null=True, verbose_name='Email')),
                ('active', models.BooleanField(blank=True, default=True, null=True, verbose_name='Actif')),
                ('signature', models.ImageField(blank=True, null=True, upload_to='vac/signature')),
            ],
            options={
                'verbose_name': 'Vacataire',
                'verbose_name_plural': 'Vacataires',
                'ordering': ['name'],
                'unique_together': {('name', 'forname')},
            },
        ),
        migrations.CreateModel(
            name='Vacation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, default='VAC', max_length=10, null=True, verbose_name='Type')),
                ('description', models.TextField(blank=True, default='', max_length=200, null=True, verbose_name='Résumé')),
                ('title', models.CharField(default='VAC :  ', max_length=100, verbose_name='Vacation')),
                ('start', models.DateField(verbose_name='Début')),
                ('start_time', models.TimeField(default='00:07:45', verbose_name='Heure début')),
                ('end', models.DateField(blank=True, null=True, verbose_name='Fin')),
                ('end_time', models.TimeField(default='00:00:00', verbose_name='Heure Fin')),
                ('is_cancelled', models.BooleanField(blank=True, default=False)),
                ('all_day', models.BooleanField(blank=True, default=False)),
                ('calendrier', models.ForeignKey(blank=True, default=4, null=True, on_delete=django.db.models.deletion.CASCADE, to='subdivision.calendrier', verbose_name='Calendrier')),
                ('vacataire', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vacataire', to='vacations.vacataire', verbose_name='Vacataire')),
            ],
            options={
                'verbose_name': 'Vacation',
                'verbose_name_plural': 'Vacations',
                'ordering': ['start', 'end'],
                'unique_together': {('vacataire', 'start')},
            },
        ),
    ]

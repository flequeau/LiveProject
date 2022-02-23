from datetime import timedelta, time

from django.db import models
from django.urls import reverse

from subdivision.models import Calendrier, WebColor


class Vacataire(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nom')
    forname = models.CharField(max_length=50, verbose_name='Prénom')
    adress1 = models.CharField(max_length=50, blank=True, null=True, verbose_name='Adresse')
    adress2 = models.CharField(max_length=50, blank=True, null=True, verbose_name='Complément d\'adresse')
    town = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ville')
    postalcode = models.CharField(max_length=10, blank=True, null=True, verbose_name='Code postal')
    telmob = models.CharField(max_length=20, blank=True, null=True, verbose_name='Tél. Mobile')
    tel2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='Tél. Perso')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='Email')
    active = models.BooleanField(verbose_name="Actif", default=True, blank=True, null=True)
    signature = models.ImageField(upload_to='vac/signature', blank=True, null=True, )
    color = models.ForeignKey(WebColor, blank=True, null=True, verbose_name='Couleur', on_delete=models.DO_NOTHING)

    def get_absolute_url(self):
        return reverse('vacataire_detail', kwargs={'pk': self.pk})

    @property
    def initials(self):
        return self.forname[2] + '.' + self.name[2]

    def __str__(self):
        return self.name + ' ' + self.forname

    class Meta:
        verbose_name = "Vacataire"
        verbose_name_plural = "Vacataires"
        ordering = ['name', ]
        unique_together = ['name', 'forname']


class Vacation(models.Model):
    type = models.CharField(blank=True, null=True, default='VAC', max_length=10, verbose_name='Type')
    description = models.TextField(max_length=200, null=True, blank=True, default='', verbose_name='Résumé')
    title = models.CharField(max_length=100, default='VAC :  ', verbose_name='Vacation')
    start = models.DateField(verbose_name='Début')
    start_time = models.TimeField(verbose_name='Heure début', default='07:45:00')
    end = models.DateField(verbose_name='Fin', null=True, blank=True)
    end_time = models.TimeField(verbose_name='Heure Fin', default='15:00:00')
    calendrier = models.ForeignKey(Calendrier, on_delete=models.CASCADE, default=4, blank=True, null=True,
                                   verbose_name='Calendrier')
    is_cancelled = models.BooleanField(default=False, blank=True)
    all_day = models.BooleanField(default=False, blank=True)
    vacataire = models.ForeignKey(Vacataire, on_delete=models.CASCADE, related_name='vacataire',
                                  verbose_name='Vacataire', null=True, blank=True)
    color = models.ForeignKey(Vacataire, related_name='Couleur', null=True, blank=True, on_delete=models.DO_NOTHING)

    @property
    def duration(self):
        t1 = timedelta(hours=self.start_time.hour, minutes=self.start_time.minute)
        t2 = timedelta(hours=self.end_time.hour, minutes=self.end_time.minute)
        secondes = (t2 - t1).seconds
        minutes = (secondes // 60) % 60
        heures = int(secondes / 3600)
        duration = time(heures, minutes)
        return duration

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.start) + ' ' + self.title

    class Meta:
        verbose_name = 'Vacation'
        verbose_name_plural = 'Vacations'
        ordering = ['-start', '-start_time']
        unique_together = [('vacataire', 'start'), ]

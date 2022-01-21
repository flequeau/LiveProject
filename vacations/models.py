from datetime import timedelta

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
    start_time = models.TimeField(verbose_name='Heure début', default='00:07:45')
    end = models.DateField(verbose_name='Fin', null=True, blank=True)
    end_time = models.TimeField(verbose_name='Heure Fin', default='00:00:00')
    calendrier = models.ForeignKey(Calendrier, on_delete=models.CASCADE, default=4, blank=True, null=True,
                                   verbose_name='Calendrier')
    is_cancelled = models.BooleanField(default=False, blank=True)
    all_day = models.BooleanField(default=True, blank=True)
    vacataire = models.ForeignKey(Vacataire, on_delete=models.CASCADE, related_name='vacataire',
                                  verbose_name='Vacataire', null=True, blank=True)

    def get_absolute_url(self):
        return reverse('vacation_detail', kwargs={'pk': self.pk})

    @property
    def jend(self):
        return self.end - timedelta(days=1)

    def __str__(self):
        return str(self.start) + ' ' + self.title

    class Meta:
        verbose_name = 'Vacation'
        verbose_name_plural = 'Vacations'
        ordering = ['start', 'end']
        unique_together = [('vacataire', 'start'), ]
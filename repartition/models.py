from django.db import models
from django.urls import reverse
from subdivision.models import Are, Rpt, Calendrier

PERIOD = [
    ('Matin', 'Matin'),
    ('Apm', 'Après-midi')
]


class HourChoice(models.Model):
    heure = models.CharField(max_length=5, null=True, blank=True, verbose_name='Heure')
    period = models.CharField(max_length=10, choices=PERIOD, blank=True, null=True, verbose_name='Période')

    def __str__(self):
        return '{}'.format(self.heure)

    class Meta:
        verbose_name = 'Heure'
        verbose_name_plural = 'Heures'
        ordering = ['heure']


class Sector(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Secteur'
        ordering = ['name']


class Room(models.Model):
    number = models.CharField(max_length=10, blank=True, null=True)
    sector = models.ForeignKey(Sector, blank=True, null=True, on_delete=models.CASCADE)
    sortnum = models.IntegerField(null=True, blank=True, unique=True)
    exportnum = models.IntegerField(null=True, blank=True, unique=True)

    def __str__(self):
        return '{}'.format(self.number)

    class Meta:
        verbose_name = 'Salle'
        ordering = ['sortnum']


class Operator(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    forname = models.CharField(max_length=50, blank=True, null=True)
    speciality = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    secretary = models.CharField(max_length=20, blank=True, null=True)
    gsm = models.CharField(max_length=20, blank=True, null=True)
    zone = models.CharField(max_length=2, blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Opérateur'
        verbose_name_plural = 'Opérateurs'
        ordering = ['name']


class Iade(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom")
    forname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Prénom")
    phone_hop = models.CharField(max_length=5, blank=True, null=True, verbose_name="Poste")
    telmob = models.CharField(max_length=12, blank=True, null=True, verbose_name="Tél. Mob.")
    email = models.EmailField(blank=True, null=True)

    STATUT = (
        ('Salarié', 'Salarié'),
        ('Vacataire', 'Vacataire')
    )
    statut = models.CharField(choices=STATUT, max_length=12, blank=True, null=True, verbose_name="Statut")

    def get_absolute_url(self):
        return reverse('iade_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {}'.format(self.forname, self.name)

    class Meta:
        verbose_name = 'IADE'
        verbose_name_plural = 'IADEs'
        ordering = ['name']


class Interne(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name="Nom")
    forname = models.CharField(max_length=50, blank=True, null=True, verbose_name="Prénom")
    telmob = models.CharField(max_length=12, blank=True, null=True, verbose_name="Tél. Mob.")
    email = models.EmailField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse('int_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {}'.format(self.forname, self.name)

    class Meta:
        verbose_name = 'Interne'
        verbose_name_plural = 'Internes'
        ordering = ['name']


class DeskRoom(models.Model):
    number = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return 'Cs {}'.format(self.number)

    class Meta:
        verbose_name = 'Salle Consultation'
        ordering = ['number']


class RepartEvent(models.Model):
    type = models.CharField(blank=True, null=True, default='RPT', max_length=10, verbose_name='Type')
    description = models.TextField(max_length=200, null=True, blank=True, default='', verbose_name='Résumé')
    title = models.CharField(max_length=100, default='Répartition :  ', verbose_name='Répartition')
    start = models.DateField(verbose_name='Date', unique=True)
    start_time = models.TimeField(verbose_name='Heure début', default='00:00:00')
    end = models.DateField(verbose_name='Fin', null=True, blank=True)
    end_time = models.TimeField(verbose_name='Heure Fin', default='00:00:00')
    calendrier = models.ForeignKey(Calendrier, default=3, on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='Calendrier')
    is_cancelled = models.BooleanField(default=False, blank=True)
    all_day = models.BooleanField(default=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    duty = models.ForeignKey(Are, related_name='are_repart', verbose_name='Anesthésiste', on_delete=models.DO_NOTHING,
                             null=True, blank=True)
    sspi = models.ForeignKey(Are, related_name='sspi', verbose_name='SSPI', on_delete=models.DO_NOTHING,
                             null=True, blank=True)

    def get_absolute_url(self):
        return reverse('repdetail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.start) + ' ' + self.title

    class Meta:
        verbose_name = 'Répartition'
        verbose_name_plural = 'Répartitions'
        ordering = ['-start']


class RepartLine(models.Model):
    repart = models.ForeignKey(RepartEvent, related_name='repartition', on_delete=models.CASCADE)
    are = models.ForeignKey(Are, related_name='repart_are', on_delete=models.DO_NOTHING, null=True, blank=True,
                            verbose_name='Anesthésiste')
    rpt = models.ForeignKey(Rpt, related_name='repart_rpt', on_delete=models.DO_NOTHING, null=True, blank=True,
                            verbose_name='Remplaçant')
    iade = models.ForeignKey(Iade, related_name='repart_iade', on_delete=models.DO_NOTHING, null=True, blank=True,
                             verbose_name='IADE')
    interne = models.ForeignKey(Interne, related_name='repart_int', on_delete=models.DO_NOTHING, null=True, blank=True,
                                verbose_name='Interne')
    operator = models.ForeignKey(Operator, related_name='operator', on_delete=models.DO_NOTHING, null=True, blank=True,
                                 verbose_name='Opérateur')
    start_time = models.ForeignKey(HourChoice, related_name='heuredebut', null=True, blank=True, verbose_name='Heure',
                                   on_delete=models.DO_NOTHING)
    room = models.ForeignKey(Room, related_name='room', null=True, blank=True, on_delete=models.DO_NOTHING,
                             verbose_name='Salle')
    period = models.CharField(max_length=10, choices=PERIOD, blank=True, null=True, verbose_name='Période')

    def get_absolute_url(self):
        return reverse('linerepdetail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {} {}'.format(self.repart.start, self.room.number, self.room.sector)

    class Meta:
        verbose_name = 'Ligne répartition'
        verbose_name_plural = 'Lignes répartitions'
        ordering = ['-repart', 'room']
        unique_together = ['repart', 'room', 'period']


class RepartCs(models.Model):
    repart = models.ForeignKey(RepartEvent, related_name='cs_repart', on_delete=models.CASCADE)
    are = models.ForeignKey(Are, related_name='cs_are', on_delete=models.DO_NOTHING, null=True, blank=True,
                            verbose_name='ARE Cs')
    deskroom = models.ForeignKey(DeskRoom, related_name='cs_deskroom', null=True, blank=True,
                                 on_delete=models.DO_NOTHING, verbose_name='Salle Cs')
    period = models.CharField(max_length=10, choices=PERIOD, blank=True, null=True, verbose_name='Période Cs')

    def get_absolute_url(self):
        return reverse('linecsdetail', kwargs={'pk': self.pk})

    def __str__(self):
        return '{} {}'.format(self.deskroom.number, self.period)

    class Meta:
        verbose_name = 'Consultation'
        verbose_name_plural = 'Consultations'
        ordering = ['-repart', 'deskroom']
        unique_together = [['repart', 'deskroom', 'period']]

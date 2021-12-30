from django.db import models
from django.urls import reverse
from datetime import timedelta
from django.conf import settings


class HopParam(models.Model):
    name = models.CharField(max_length=100)
    adress1 = models.CharField(max_length=100)
    adress2 = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100)
    postalcode = models.CharField(max_length=5)
    cedex = models.CharField(max_length=10, blank=True, null=True)
    finess = models.CharField(max_length=10, blank=True, null=True)
    logo = models.ImageField(upload_to='hop', blank=True, null=True)
    tel = models.CharField(max_length=10, blank=True, null=True)
    fax = models.CharField(max_length=10, blank=True, null=True)
    villes = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Hôpital'
        verbose_name_plural = 'Hôpitaux'
        ordering = ['name']


class WebColor(models.Model):
    color = models.CharField(max_length=30, verbose_name='Couleur')
    colorHex = models.CharField(max_length=10, verbose_name='Hexa')

    def __str__(self):
        return self.color

    class Meta:
        verbose_name = 'Couleurs Web'
        ordering = ['color']


class Calendrier(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, null=True, blank=True)
    color = models.ForeignKey(WebColor, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Calendrier'
        verbose_name_plural = 'Calendriers'
        ordering = ['name']


class Are(models.Model):
    SECTOR = (
        ('1', 'Secteur 1'),
        ('2', 'Secteur 2'),
    )

    name = models.CharField(max_length=50, verbose_name='Nom')
    forname = models.CharField(max_length=50, verbose_name='Prénom')
    adress1 = models.CharField(max_length=50, blank=True, null=True, verbose_name='Adresse')
    adress2 = models.CharField(max_length=50, blank=True, null=True, verbose_name='Complément adresse')
    town = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ville')
    coNum = models.CharField(max_length=20, blank=True, null=True, verbose_name='Numéro CO')
    rpps = models.CharField(max_length=20, blank=True, null=True, verbose_name='Rpps')
    postalcode = models.CharField(max_length=5, blank=True, null=True, verbose_name='Code postal')
    telmob = models.CharField(max_length=20, blank=True, null=True, verbose_name='Tél. Mobile')
    tel2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='Tél. Perso.')
    phone_hop = models.CharField(max_length=12, verbose_name='Poste', blank=True, null=True)
    phone_secretary = models.CharField(max_length=12, verbose_name='Secrétariat', null=True, blank=True)
    email = models.EmailField(max_length=50, blank=True, null=True)
    secteur = models.CharField(max_length=10, choices=SECTOR, verbose_name='Secteur', default=True, blank=True,
                               null=True)
    photo = models.ImageField(upload_to='are/photo', blank=True, null=True)
    signature = models.ImageField(upload_to='are/signature', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('are_detail', kwargs={'pk': self.pk})

    @property
    def initials(self):
        return self.forname[2] + '.' + self.name[2]

    def __str__(self):
        return self.name + ' ' + self.forname

    class Meta:
        verbose_name = "Anesthésiste"
        verbose_name_plural = "Anesthésistes"
        ordering = ['name', ]


class Rpt(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nom')
    forname = models.CharField(max_length=50, verbose_name='Prénom')
    adress1 = models.CharField(max_length=50, blank=True, null=True, verbose_name='Adresse')
    adress2 = models.CharField(max_length=50, blank=True, null=True, verbose_name='Complément d\'adresse')
    town = models.CharField(max_length=50, blank=True, null=True, verbose_name='Ville')
    codepartname = models.CharField(max_length=50, blank=True, null=True, verbose_name='Nom Départ. CO')
    codepartnum = models.CharField(max_length=10, blank=True, null=True, verbose_name='Num. Départ. CO')
    conum = models.CharField(max_length=50, blank=True, null=True, verbose_name='Num. CO')
    rpps = models.CharField(max_length=20, blank=True, null=True, verbose_name='Num. RPPS')
    urssafnum = models.CharField(max_length=50, blank=True, null=True, verbose_name='URSSAF')
    sirennum = models.CharField(max_length=50, blank=True, null=True, verbose_name='Siren')
    postalcode = models.CharField(max_length=10, blank=True, null=True, verbose_name='Code postal')
    telmob = models.CharField(max_length=20, blank=True, null=True, verbose_name='Tél. Mobile')
    tel2 = models.CharField(max_length=20, blank=True, null=True, verbose_name='Tél. Perso')
    tel3 = models.CharField(max_length=20, blank=True, null=True, verbose_name='Tél. Travail')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='Email')
    status = models.BooleanField(verbose_name='Thésé', default=True, blank=True, null=True)
    photo = models.ImageField(upload_to='rpt/photo', blank=True, null=True, verbose_name='Photo')
    assurance = models.FileField(upload_to='rpt/assurance', blank=True, null=True, verbose_name='Assurance')
    licence = models.FileField(upload_to='rpt/licence', blank=True, null=True, verbose_name='Licence')
    licence_exp_date = models.DateField(verbose_name='Date expiration licence', blank=True, null=True)
    active = models.BooleanField(verbose_name="Actif", default=True, blank=True, null=True)
    signature = models.ImageField(upload_to='rpt/signature', blank=True, null=True, )

    def get_absolute_url(self):
        return reverse('rpt_detail', kwargs={'pk': self.pk})

    @property
    def initials(self):
        return self.forname[2] + '.' + self.name[2]

    def __str__(self):
        return self.name + ' ' + self.forname

    class Meta:
        verbose_name = "Remplaçant"
        verbose_name_plural = "Remplaçants"
        ordering = ['name', ]
        unique_together = ['name', 'forname']


class Event(models.Model):
    PAYTYPE = (
        ('C', 'Chèque'),
        ('V', 'Virement'),
    )

    type = models.CharField(blank=True, null=True, default='RPT', max_length=10, verbose_name='Type')
    description = models.TextField(max_length=200, null=True, blank=True, default='', verbose_name='Résumé')
    title = models.CharField(max_length=100, default='RPT :  ', verbose_name='Titre')
    start = models.DateField(verbose_name='Début')
    start_time = models.TimeField(verbose_name='Heure début', default='00:00:00')
    end = models.DateField(verbose_name='Fin', null=True, blank=True)
    end_time = models.TimeField(verbose_name='Heure Fin', default='00:00:00')
    calendrier = models.ForeignKey(Calendrier, on_delete=models.CASCADE, blank=True, null=True,
                                   verbose_name='Type édition')
    is_cancelled = models.BooleanField(default=False, blank=True)
    all_day = models.BooleanField(default=True, blank=True)
    are = models.ForeignKey(Are, on_delete=models.DO_NOTHING, related_name='are', verbose_name='Anesthésiste',
                            null=True)
    rpt = models.ForeignKey(Rpt, on_delete=models.DO_NOTHING, related_name='rpt', verbose_name='Remplaçant', null=True)
    pay_date = models.DateField(blank=True, null=True, verbose_name='Date de paiement')
    pay_type = models.CharField(max_length=20, choices=PAYTYPE, blank=True, null=True, verbose_name='Moyen de paiement')
    pay_are = models.ForeignKey(Are, related_name='ArePay', null=True, blank=True, on_delete=models.DO_NOTHING,
                                verbose_name='Payeur')
    pay_amount = models.IntegerField(default=settings.AMOUNT_RPT, blank=True, null=True, verbose_name='Montant')
    pay_numchq = models.CharField(max_length=50, null=True, blank=True, verbose_name='N° chèque')

    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'pk': self.pk})

    @property
    def jend(self):
        return self.end - timedelta(days=1)

    def __str__(self):
        return str(self.start) + ' ' + self.title

    class Meta:
        verbose_name = 'Evènement'
        verbose_name_plural = 'Evènements'
        ordering = ['start', 'end']
        unique_together = [('are', 'start'), ('rpt', 'start')]

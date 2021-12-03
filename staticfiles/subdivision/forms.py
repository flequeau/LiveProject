from django import forms
from django.forms import ModelForm
from .models import Event, Rpt
from datetime import datetime, timedelta

MOIS = [
    ('01', 'Janvier'),
    ('02', 'Février'),
    ('03', 'Mars'),
    ('04', 'Avril'),
    ('05', 'Mai'),
    ('06', 'Juin'),
    ('07', 'Juillet'),
    ('08', 'Août'),
    ('09', 'Septembre'),
    ('10', 'Octobre'),
    ('11', 'Novembre'),
    ('12', 'Décembre'),
]


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'are', 'rpt', 'start', 'end', 'calendrier', 'pay_amount', 'pay_are',
                  'pay_type', 'pay_numchq', 'pay_date')


class SearchRptMonthForm(forms.Form):
    today = datetime.now()
    anneeprev = today - timedelta(weeks=52)
    anneefin = today + timedelta(weeks=104)
    rpt = forms.ModelChoiceField(queryset=Rpt.objects.all())
    annee = forms.ChoiceField(choices=[(x, x) for x in range(anneeprev.year, anneefin.year)])
    mois = forms.ChoiceField(choices=MOIS)


class SearchMonthForm(forms.Form):
    today = datetime.now()
    anneeprev = today - timedelta(weeks=52)
    anneefin = today + timedelta(weeks=104)
    annee = forms.ChoiceField(choices=[(x, x) for x in range(anneeprev.year, anneefin.year)])
    mois = forms.ChoiceField(choices=MOIS)

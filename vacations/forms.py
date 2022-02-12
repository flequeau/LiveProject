from django import forms
from django.forms import ModelForm
from .models import Vacation, Vacataire
from datetime import datetime, timedelta



class VacForm(ModelForm):
    class Meta:
        model = Vacation
        fields = (
            'title', 'start', 'start_time', 'end', 'end_time', 'vacataire'
        )

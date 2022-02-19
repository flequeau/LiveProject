from django.forms import ModelForm
from .models import Vacation
from django.forms import ModelForm

from .models import Vacation


class VacForm(ModelForm):
    class Meta:
        model = Vacation
        fields = (
            'title', 'start', 'start_time', 'end', 'end_time', 'vacataire'
        )

from django import forms
from django.forms import ModelForm
from .models import RepartEvent, RepartLine, RepartCs


class EventFormRepart(ModelForm):
    class Meta:
        model = RepartEvent
        fields = ('title', 'duty', 'sspi', 'start', 'description')
        widgets = {
            'description': forms.Textarea(attrs={
                'style': 'height: 50px;'}),
        }


class RepartLineForm(ModelForm):
    class Meta:
        model = RepartLine
        fields = ('room', 'start_time', 'operator', 'are', 'rpt', 'iade', 'interne')


class RepartLineApmForm(ModelForm):
    class Meta:
        model = RepartLine
        fields = ('room', 'start_time', 'operator', 'are', 'rpt', 'iade', 'interne')


class CsLineForm(ModelForm):
    class Meta:
        model = RepartCs
        fields = ( 'deskroom','are')

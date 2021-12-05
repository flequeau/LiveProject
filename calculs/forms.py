from django import forms

GENRE = (
    (0, '-----'),
    (75, 'Monsieur'),
    (65, 'Madame'),
)

HEMATFINAL = (
    (0, '-----'),
    (0.28, '0,28'),
    (0.30, '0,30')
)

BLOODLOSS = (
    (0, '-----'),
    (650, 'Prothèse totale hanche'),
    (650, 'Prothèse totale genou'),
    (350, 'Prothèse totale épaule'),
)


class BloodSaveForm(forms.Form):
    gender = forms.ChoiceField(choices=GENRE, label='Genre', required=True)
    weight = forms.IntegerField(label='Poids en kg', required=True)
    hemacrit_init = forms.FloatField(label='Hématocrite initial', widget=forms.NumberInput(
        attrs={'step': '0.01'}), required=True)
    hemacrit_final = forms.ChoiceField(choices=HEMATFINAL, label='Hématocrite final', required=True)
    blood_loss = forms.ChoiceField(choices=BLOODLOSS, label='Pertes sanguines prévues', required=True)

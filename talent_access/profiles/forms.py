from django import forms
from .models import ProfilPME


class ProfilPMEForm(forms.ModelForm):
    class Meta:
        model = ProfilPME
        exclude = ('utilisateur',)

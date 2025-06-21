from django import forms
from .models import Candidature, OffreEmploi


class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ["lettre_motivation"]
        widgets = {
            "lettre_motivation": forms.Textarea(attrs={"class": "form-control"}),
        }


class OffreForm(forms.ModelForm):
    class Meta:
        model = OffreEmploi
        fields = ["titre", "description", "type_contrat", "localisation"]
        widgets = {
            "titre": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "type_contrat": forms.TextInput(attrs={"class": "form-control"}),
            "localisation": forms.TextInput(attrs={"class": "form-control"}),
        }

from django import forms
from .models import Candidature


class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ["lettre_motivation"]
        widgets = {
            "lettre_motivation": forms.Textarea(attrs={"class": "form-control"}),
        }

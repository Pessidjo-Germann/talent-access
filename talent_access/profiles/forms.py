from django import forms
from django.forms import inlineformset_factory
from .models import (
    ProfilDiplome,
    Competence,
    FormationExperience,
    ProfilPME,
)


class ProfilDiplomeForm(forms.ModelForm):
    class Meta:
        model = ProfilDiplome
        exclude = ("utilisateur",)


CompetenceFormSet = inlineformset_factory(
    ProfilDiplome,
    Competence,
    fields=("nom", "niveau"),
    extra=1,
    can_delete=True,
)

FormationExperienceFormSet = inlineformset_factory(
    ProfilDiplome,
    FormationExperience,
    fields=("diplome_obtenu", "date_obtention", "duree_formation"),
    extra=1,
    can_delete=True,
)


class ProfilPMEForm(forms.ModelForm):
    class Meta:
        model = ProfilPME
        exclude = ("utilisateur",)

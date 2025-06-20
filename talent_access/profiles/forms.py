from django import forms
from django.forms import inlineformset_factory
from .models import ProfilDiplome, Competence, FormationExperience


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

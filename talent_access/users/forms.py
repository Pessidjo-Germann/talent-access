from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Utilisateur

class DiplomeSignupForm(UserCreationForm):
    niveau_etude = forms.CharField(max_length=100, required=False, label="Niveau d'étude")

    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = ("email", "first_name", "last_name", "niveau_etude")

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        user.username = email
        user.email = email
        user.statut = Utilisateur.Statut.DIPLOME
        if commit:
            user.save()
        return user

class PMESignupForm(UserCreationForm):
    company_name = forms.CharField(max_length=255, label="Nom de l'entreprise")
    sector = forms.CharField(max_length=255, label="Secteur d'activité")

    class Meta(UserCreationForm.Meta):
        model = Utilisateur
        fields = ("email", "company_name", "sector")

    def save(self, commit=True):
        user = super().save(commit=False)
        email = self.cleaned_data.get("email")
        user.username = email
        user.email = email
        user.first_name = self.cleaned_data.get("company_name")
        user.last_name = self.cleaned_data.get("sector")
        user.statut = Utilisateur.Statut.PME
        if commit:
            user.save()
        return user

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from users.models import Utilisateur
from .forms import (
    CompetenceFormSet,
    FormationExperienceFormSet,
    ProfilDiplomeForm,
)
from .models import ProfilDiplome


@login_required
def voir_profil_diplome(request):
    if request.user.statut != Utilisateur.Statut.DIPLOME:
        return redirect("pme_dashboard")
    profil = ProfilDiplome.objects.filter(utilisateur=request.user).first()
    competences = []
    formations = []
    if profil:
        competences = profil.competence_set.all()
        formations = profil.formationexperience_set.all()
    context = {
        "profil": profil,
        "competences": competences,
        "formations": formations,
    }
    return render(request, "profil_diplome.html", context)


@login_required
def modifier_profil_diplome(request):
    if request.user.statut != Utilisateur.Statut.DIPLOME:
        return redirect("pme_dashboard")
    profil = ProfilDiplome.objects.filter(utilisateur=request.user).first()
    if request.method == "POST":
        form = ProfilDiplomeForm(request.POST, request.FILES, instance=profil)
        comp_formset = CompetenceFormSet(request.POST, instance=profil)
        form_formset = FormationExperienceFormSet(request.POST, instance=profil)
        if form.is_valid() and comp_formset.is_valid() and form_formset.is_valid():
            profil = form.save(commit=False)
            profil.utilisateur = request.user
            profil.save()
            comp_formset.instance = profil
            form_formset.instance = profil
            comp_formset.save()
            form_formset.save()
            messages.success(request, "Profil mis à jour")
            return redirect("voir_profil_diplome")
    else:
        form = ProfilDiplomeForm(instance=profil)
        comp_formset = CompetenceFormSet(instance=profil)
        form_formset = FormationExperienceFormSet(instance=profil)
    context = {
        "form": form,
        "competence_formset": comp_formset,
        "formation_formset": form_formset,
    }
    return render(request, "modifier_profil_diplome.html", context)

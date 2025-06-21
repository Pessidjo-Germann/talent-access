from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.models import Utilisateur
from .models import ProfilPME
from .forms import ProfilPMEForm


@login_required
def voir_profil_pme(request):
    if request.user.statut != Utilisateur.Statut.PME:
        return redirect("diplome_dashboard")
    profil = ProfilPME.objects.filter(utilisateur=request.user).first()
    return render(request, "profil_pme.html", {"profil": profil})


@login_required
def modifier_profil_pme(request):
    if request.user.statut != Utilisateur.Statut.PME:
        return redirect("diplome_dashboard")
    profil, _ = ProfilPME.objects.get_or_create(utilisateur=request.user)
    if request.method == "POST":
        form = ProfilPMEForm(request.POST, request.FILES, instance=profil)
        if form.is_valid():
            form.instance.utilisateur = request.user
            form.save()
            messages.success(request, "Profil mis à jour.")
            return redirect("voir_profil_pme")
    else:
        form = ProfilPMEForm(instance=profil)
    return render(request, "modifier_profil_pme.html", {"form": form})



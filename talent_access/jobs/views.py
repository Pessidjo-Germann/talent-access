from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from users.models import Utilisateur
from .forms import CandidatureForm
from .models import Candidature, OffreEmploi


@login_required
def postuler_offre(request, offre_id):
    if request.user.statut != Utilisateur.Statut.DIPLOME:
        return redirect("diplome_login")

    offre = get_object_or_404(OffreEmploi, id=offre_id)

    if Candidature.objects.filter(offre=offre, candidat=request.user).exists():
        messages.warning(request, "Vous avez déjà postulé à cette offre.")
        return redirect("mes_candidatures")

    if request.method == "POST":
        form = CandidatureForm(request.POST)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.offre = offre
            candidature.candidat = request.user
            candidature.save()
            messages.success(request, "Candidature envoyée.")
            return redirect("mes_candidatures")
    else:
        form = CandidatureForm()

    return render(request, "postuler_offre.html", {"form": form, "offre": offre})


@login_required
def mes_candidatures(request):
    if request.user.statut != Utilisateur.Statut.DIPLOME:
        return redirect("pme_dashboard")

    candidatures = (
        Candidature.objects.filter(candidat=request.user)
        .select_related("offre")
        .order_by("-date_candidature")
    )
    return render(
        request,
        "mes_candidatures.html",
        {"candidatures": candidatures},
    )


@login_required
def candidatures_recues(request):
    if request.user.statut != Utilisateur.Statut.PME:
        return redirect("diplome_dashboard")

    if request.method == "POST":
        cand_id = request.POST.get("candidature_id")
        statut = request.POST.get("statut")
        candidature = get_object_or_404(
            Candidature,
            id=cand_id,
            offre__entreprise=request.user,
        )
        if statut in dict(Candidature.Statut.choices).keys():
            candidature.statut = statut
            candidature.save()

    candidatures = (
        Candidature.objects.filter(offre__entreprise=request.user)
        .select_related("offre", "candidat")
        .order_by("-date_candidature")
    )
    return render(
        request,
        "candidatures_reçues.html",
        {"candidatures": candidatures},
    )

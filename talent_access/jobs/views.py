from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from users.models import Utilisateur
from .forms import CandidatureForm, OffreForm
from .models import Candidature, OffreEmploi
from profiles.models import ProfilDiplome


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


@login_required
def candidature_detail(request, candidature_id):
    """Allow a PME to view and update a candidature."""
    if request.user.statut != Utilisateur.Statut.PME:
        return redirect("diplome_dashboard")

    candidature = get_object_or_404(
        Candidature.objects.select_related("offre", "candidat"),
        id=candidature_id,
        offre__entreprise=request.user,
    )
    profil = ProfilDiplome.objects.filter(utilisateur=candidature.candidat).first()

    if request.method == "POST":
        statut = request.POST.get("statut")
        if statut in dict(Candidature.Statut.choices).keys():
            candidature.statut = statut
            candidature.save()
            messages.success(request, "Statut mis à jour.")
            return redirect("candidature_detail", candidature_id=candidature.id)

    return render(
        request,
        "candidature_detail.html",
        {"candidature": candidature, "profil": profil, "statuts": Candidature.Statut.choices},
    )


@login_required
def creer_offre(request):
    if request.user.statut != Utilisateur.Statut.PME:
        return redirect("diplome_dashboard")

    if request.method == "POST":
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.entreprise = request.user
            offre.save()
            messages.success(request, "Offre créée.")
            return redirect("pme_dashboard")
    else:
        form = OffreForm()

    return render(request, "creer_offre.html", {"form": form})


@login_required
def offre_detail(request, offre_id):
    """Display the detail of a job offer for graduates."""
    if request.user.statut != Utilisateur.Statut.DIPLOME:
        return redirect("pme_dashboard")

    offre = get_object_or_404(OffreEmploi, id=offre_id)
    deja_postule = Candidature.objects.filter(offre=offre, candidat=request.user).exists()
    return render(
        request,
        "offre_detail.html",
        {"offre": offre, "deja_postule": deja_postule},
    )


@login_required
def offre_pme_detail(request, offre_id):
    """Display details of an offer for its PME owner."""
    if request.user.statut != Utilisateur.Statut.PME:
        return redirect("diplome_dashboard")

    offre = get_object_or_404(OffreEmploi, id=offre_id, entreprise=request.user)
    return render(request, "offre_pme_detail.html", {"offre": offre})


@login_required
def modifier_offre(request, offre_id):
    """Allow a PME to edit one of its job offers."""
    if request.user.statut != Utilisateur.Statut.PME:
        return redirect("diplome_dashboard")

    offre = get_object_or_404(OffreEmploi, id=offre_id, entreprise=request.user)

    if request.method == "POST":
        form = OffreForm(request.POST, instance=offre)
        if form.is_valid():
            form.save()
            messages.success(request, "Offre mise \u00e0 jour.")
            return redirect("pme_dashboard")
    else:
        form = OffreForm(instance=offre)

    return render(
        request,
        "modifier_offre.html",
        {"form": form, "offre": offre},
    )


@login_required
def liste_offres(request):
    """List all available job offers for graduates."""
    if request.user.statut != Utilisateur.Statut.DIPLOME:
        return redirect("pme_dashboard")

    offres = OffreEmploi.objects.all().order_by("-date_publication")
    return render(request, "liste_offres.html", {"offres": offres})

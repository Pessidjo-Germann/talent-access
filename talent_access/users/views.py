from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import DiplomeSignupForm, PMESignupForm, EmailAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Utilisateur
from jobs.models import OffreEmploi, Candidature
from profiles.models import ProfilDiplome


def home(request):
    """Render the application home page."""
    return render(request, "home.html")


def diplome_signup(request):
    if request.method == "POST":
        form = DiplomeSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie.")
            return redirect("diplome_dashboard")
        messages.error(request, "Inscription échouée.")
    else:
        form = DiplomeSignupForm()
    return render(request, "diplome_signup.html", {"form": form})


def pme_signup(request):
    if request.method == "POST":
        form = PMESignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie.")
            return redirect("pme_dashboard")
        messages.error(request, "Inscription échouée.")
    else:
        form = PMESignupForm()
    return render(request, "pme_signup.html", {"form": form})


def diplome_login(request):
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user.statut != Utilisateur.Statut.DIPLOME:
            form.add_error(None, "Ce compte n'est pas un compte Diplômé.")
        else:
            login(request, user)
            return redirect("diplome_dashboard")
    return render(request, "diplome_login.html", {"form": form})


def pme_login(request):
    form = EmailAuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        if user.statut != Utilisateur.Statut.PME:
            form.add_error(None, "Ce compte n'est pas un compte PME.")
        else:
            login(request, user)
            return redirect("pme_dashboard")
    return render(request, "pme_login.html", {"form": form})


@login_required
def diplome_dashboard(request):
    if request.user.statut != Utilisateur.Statut.DIPLOME:
        return redirect("pme_dashboard")
    profil = None
    try:
        from profiles.models import ProfilDiplome
        profil = ProfilDiplome.objects.filter(utilisateur=request.user).first()
    except Exception:
        profil = None

    try:
        from jobs.models import OffreEmploi, Candidature
        offres = OffreEmploi.objects.all()
        candidatures = (
            Candidature.objects.filter(candidat=request.user)
            .select_related("offre")
        )
    except Exception:
        offres = []
        candidatures = []

    context = {
        "profil": profil,
        "offres": offres,
        "candidatures": candidatures,
    }
    return render(request, "diplome_dashboard.html", context)


@login_required
def pme_dashboard(request):
    if request.user.statut != Utilisateur.Statut.PME:
        return redirect("diplome_dashboard")
    offres = (
        OffreEmploi.objects.filter(entreprise=request.user)
        .order_by("-date_publication")
    )
    candidatures = (
        Candidature.objects.filter(offre__entreprise=request.user)
        .select_related("candidat", "offre")
        .order_by("-date_candidature")
    )
    from profiles.models import ProfilDiplome
    for cand in candidatures:
        cand.profil = ProfilDiplome.objects.filter(utilisateur=cand.candidat).first()
    return render(
        request,
        "pme_dashboard.html",
        {
            "offres": offres,
            "candidatures": candidatures,
        },
    )

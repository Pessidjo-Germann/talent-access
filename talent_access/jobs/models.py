from django.db import models
from users.models import Utilisateur


class OffreEmploi(models.Model):
    entreprise = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    titre = models.CharField(max_length=255)
    description = models.TextField()
    type_contrat = models.CharField(max_length=100)
    localisation = models.CharField(max_length=255)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titre


class Candidature(models.Model):
    class Statut(models.TextChoices):
        EN_ATTENTE = "en_attente", "en attente"
        ACCEPTEE = "acceptée", "acceptée"
        REFUSEE = "refusée", "refusée"

    offre = models.ForeignKey(OffreEmploi, on_delete=models.CASCADE)
    candidat = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_candidature = models.DateTimeField(auto_now_add=True)
    lettre_motivation = models.TextField(blank=True)
    statut = models.CharField(
        max_length=20, choices=Statut.choices, default=Statut.EN_ATTENTE
    )

    def __str__(self):
        return f"Candidature de {self.candidat.username}"

from django.db import models
from users.models import Utilisateur


class ProfilDiplome(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    numero_telephone = models.CharField(max_length=20)
    adresse = models.CharField(max_length=255)
    date_naissance = models.DateField()
    niveau_etude = models.CharField(max_length=100)
    cv = models.FileField(upload_to='cvs/', blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.utilisateur.username}"


class Competence(models.Model):
    class Niveau(models.TextChoices):
        DEBUTANT = 'DEBUTANT', 'débutant'
        INTERMEDIAIRE = 'INTERMEDIAIRE', 'intermédiaire'
        AVANCE = 'AVANCE', 'avancé'

    profil_diplome = models.ForeignKey(ProfilDiplome, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    niveau = models.CharField(max_length=20, choices=Niveau.choices)

    def __str__(self):
        return self.nom


class FormationExperience(models.Model):
    profil_diplome = models.ForeignKey(ProfilDiplome, on_delete=models.CASCADE)
    diplome_obtenu = models.CharField(max_length=255)
    date_obtention = models.DateField()
    duree_formation = models.CharField(max_length=100)

    def __str__(self):
        return self.diplome_obtenu

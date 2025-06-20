from django.contrib.auth.models import AbstractUser
from django.db import models


class Utilisateur(AbstractUser):
    class Statut(models.TextChoices):
        DIPLOME = 'DIPLOME', 'Diplômé'
        PME = 'PME', 'PME'

    email = models.EmailField(unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=Statut.choices)

    def __str__(self):
        return self.username

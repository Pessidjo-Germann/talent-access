# Generated by Django 5.2.3 on 2025-06-20 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Competence",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100)),
                (
                    "niveau",
                    models.CharField(
                        choices=[
                            ("DEBUTANT", "débutant"),
                            ("INTERMEDIAIRE", "intermédiaire"),
                            ("AVANCE", "avancé"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FormationExperience",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("diplome_obtenu", models.CharField(max_length=255)),
                ("date_obtention", models.DateField()),
                ("duree_formation", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="ProfilDiplome",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("numero_telephone", models.CharField(max_length=20)),
                ("adresse", models.CharField(max_length=255)),
                ("date_naissance", models.DateField()),
                ("niveau_etude", models.CharField(max_length=100)),
                ("cv", models.FileField(blank=True, null=True, upload_to="cvs/")),
            ],
        ),
    ]

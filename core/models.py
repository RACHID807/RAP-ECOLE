"""
Modèles de base de données pour RAP CLASH SCHOOL (Côte d'Ivoire).
Assure la persistance complète des candidats, des votes Wave,
des duels, des établissements et des transactions financières.
"""

from django.db import models


class Categorie(models.Model):
    """Catégorie scolaire ou universitaire (Collèges, Lycées, Universités)."""
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"

    def __str__(self):
        return self.nom


class Etablissement(models.Model):
    """Établissement scolaire ou universitaire ivoirien représenté."""
    nom = models.CharField(max_length=255)
    commune = models.CharField(max_length=100)
    ville = models.CharField(max_length=100, default="Abidjan")
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='etablissements', null=True, blank=True)

    class Meta:
        verbose_name = "Établissement"
        verbose_name_plural = "Établissements"

    def __str__(self):
        return f"{self.nom} ({self.commune})"


class Candidat(models.Model):
    """Profil officiel du candidat avec photo, audio et vidéo."""
    STATUT_CHOICES = [
        ('en_attente', 'En attente de validation'),
        ('valide', 'Validé'),
        ('elimine', 'Éliminé'),
    ]

    nom_artistique = models.CharField(max_length=150)
    prenom = models.CharField(max_length=150, blank=True)
    nom = models.CharField(max_length=150, blank=True)
    etablissement = models.ForeignKey(Etablissement, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidats')
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True, related_name='candidats')
    
    # Médias
    photo_url = models.CharField(max_length=500, blank=True, help_text="URL externe ou chemin d'accès de la photo")
    photo_fichier = models.ImageField(upload_to='candidats/photos/', blank=True, null=True)
    video_url = models.CharField(max_length=500, blank=True, help_text="Lien vidéo de clash (MP4 / streaming)")
    video_titre = models.CharField(max_length=200, blank=True)
    audio_url = models.CharField(max_length=500, blank=True, help_text="Lien de l'extrait audio")
    audio_titre = models.CharField(max_length=200, blank=True)
    
    # Infos artistiques
    bio = models.TextField(blank=True)
    style = models.CharField(max_length=100, blank=True, default="Freestyle")
    votes = models.PositiveIntegerField(default=0)
    rang = models.PositiveIntegerField(default=1)
    statut = models.CharField(max_length=30, choices=STATUT_CHOICES, default='valide')
    date_inscription = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Candidat"
        verbose_name_plural = "Candidats"
        ordering = ['-votes', 'nom_artistique']

    def __str__(self):
        return f"{self.nom_artistique} ({self.etablissement.nom if self.etablissement else 'Sans école'})"


class Vote(models.Model):
    """Vote officiel soumis via Wave CI (500 FCFA)."""
    STATUT_CHOICES = [
        ('en_attente', 'En attente de pointage Wave'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]

    candidat = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='votes_recus', null=True, blank=True)
    candidat_nom = models.CharField(max_length=150, blank=True)
    votant_nom = models.CharField(max_length=150)
    votant_email = models.EmailField()
    votant_telephone = models.CharField(max_length=30, help_text="Numéro Wave utilisé pour le paiement")
    montant = models.PositiveIntegerField(default=500, help_text="Montant en FCFA")
    voix = models.PositiveIntegerField(default=1, help_text="Nombre de suffrages attribués")
    methode = models.CharField(max_length=50, default='Wave CI')
    statut = models.CharField(max_length=30, choices=STATUT_CHOICES, default='en_attente')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
    email_envoye = models.BooleanField(default=False, help_text="Courriel Brevo expédié avec succès")

    class Meta:
        verbose_name = "Vote"
        verbose_name_plural = "Votes"
        ordering = ['-id']

    def __str__(self):
        return f"Vote #{self.id} pour {self.candidat_nom} ({self.montant} FCFA) - {self.statut}"


class Duel(models.Model):
    """Affrontement en direct entre deux rappeurs."""
    STATUT_CHOICES = [
        ('programme', 'Programmé'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
    ]

    candidat1 = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='duels_en_tant_que_c1')
    candidat2 = models.ForeignKey(Candidat, on_delete=models.CASCADE, related_name='duels_en_tant_que_c2')
    titre = models.CharField(max_length=200, blank=True)
    phase = models.CharField(max_length=100, default="Quarts de Finale")
    votes1 = models.PositiveIntegerField(default=0)
    votes2 = models.PositiveIntegerField(default=0)
    statut = models.CharField(max_length=30, choices=STATUT_CHOICES, default='en_cours')
    temps_restant = models.CharField(max_length=50, default="02j 14h")
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Duel"
        verbose_name_plural = "Duels"

    def __str__(self):
        return f"{self.candidat1.nom_artistique} vs {self.candidat2.nom_artistique} ({self.phase})"


class Transaction(models.Model):
    """Historique financier des contributions Mobile Money certifiées."""
    reference = models.CharField(max_length=100, unique=True)
    vote = models.ForeignKey(Vote, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    candidat_nom = models.CharField(max_length=150)
    operateur = models.CharField(max_length=50, default="Wave CI")
    telephone = models.CharField(max_length=30)
    montant = models.PositiveIntegerField(default=500)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-date']

    def __str__(self):
        return f"{self.reference} - {self.montant} FCFA ({self.operateur})"


class Annonce(models.Model):
    """Communiqués officiels de l'arène."""
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    type_annonce = models.CharField(max_length=50, default="info")
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Annonce"
        verbose_name_plural = "Annonces"

    def __str__(self):
        return self.titre

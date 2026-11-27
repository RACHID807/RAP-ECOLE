"""
Service de synchronisation avec la base de données SQLite/PostgreSQL.
Garantit que chaque vote Wave, chaque candidat et chaque transaction
soit persisté de manière permanente sur le disque.
"""

from django.utils import timezone
from .models import Categorie, Etablissement, Candidat, Vote, Duel, Transaction, Annonce
from .data import CATEGORIES as DATA_CATEGORIES, ETABLISSEMENTS as DATA_ETABLISSEMENTS


def initialiser_base_si_vide():
    """Remplit les catégories et établissements par défaut si la base est neuve."""
    if Categorie.objects.count() == 0:
        for cat in DATA_CATEGORIES:
            Categorie.objects.create(
                id=cat['id'],
                nom=cat['nom'],
                slug=cat['slug'],
                description=cat.get('description', '')
            )

    if Etablissement.objects.count() == 0:
        for etab in DATA_ETABLISSEMENTS:
            cat_obj = Categorie.objects.filter(id=etab.get('categorie_id')).first()
            Etablissement.objects.create(
                id=etab['id'],
                nom=etab['nom'],
                commune=etab['commune'],
                ville=etab['ville'],
                categorie=cat_obj
            )


def sauvegarder_vote_db(votant_nom, votant_email, votant_telephone, candidat_id, montant=500, nb_voix=1, methode='Wave CI'):
    """Enregistre un nouveau vote de façon permanente dans la table Vote."""
    initialiser_base_si_vide()
    candidat_obj = Candidat.objects.filter(id=candidat_id).first()
    candidat_nom = candidat_obj.nom_artistique if candidat_obj else f"Candidat #{candidat_id}"

    vote = Vote.objects.create(
        candidat=candidat_obj,
        candidat_nom=candidat_nom,
        votant_nom=votant_nom,
        votant_email=votant_email,
        votant_telephone=votant_telephone,
        montant=montant,
        voix=nb_voix,
        methode=methode,
        statut='en_attente'
    )
    return vote


def valider_vote_db(vote_id):
    """Valide le vote dans la base de données et crée la transaction financière."""
    try:
        vote = Vote.objects.get(id=vote_id)
    except Vote.DoesNotExist:
        return False, "Vote introuvable en base de données."

    if vote.statut == 'valide':
        return False, "Ce vote a déjà été validé."

    vote.statut = 'valide'
    vote.date_validation = timezone.now()
    vote.save()

    # Crédit des voix au candidat
    if vote.candidat:
        vote.candidat.votes += vote.voix
        vote.candidat.save()

    # Enregistrement de la transaction
    ref = f"WAVE-{vote.id:04d}-{vote.votant_telephone[-4:] if len(vote.votant_telephone)>=4 else '0000'}"
    Transaction.objects.get_or_create(
        reference=ref,
        defaults={
            'vote': vote,
            'candidat_nom': vote.candidat_nom,
            'operateur': 'Wave CI',
            'telephone': vote.votant_telephone,
            'montant': vote.montant,
        }
    )

    return True, "Vote validé avec succès en base de données."

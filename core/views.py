"""
Vues de l'application 'core'.
Toutes les données fictives ont été retirées.
Les vues transmettent les données de la base (actuellement vides)
et gèrent proprement les cas où aucun candidat ou duel n'est encore enregistré.
"""

from django.shortcuts import render
from django.http import Http404
from .data import (
    CATEGORIES, ETABLISSEMENTS, CANDIDATS, DUELS, VOTES_PACKAGES,
    ANNONCES, STATS_GENERALES, PHASES,
    get_candidat_by_id, get_duel_by_id, enrich_candidat,
    get_all_candidats_enriched, get_all_duels_enriched,
)

# Liste des transactions réelles (initialement vide)
TRANSACTIONS = []

# ---------------------------------------------------------------------------
# 1. PAGES PUBLIQUES
# ---------------------------------------------------------------------------

def home(request):
    """
    Page d'accueil : affiche les participants et les duels actifs s'ils existent,
    ou des états d'invitation à l'inscription si la plateforme vient d'ouvrir.
    """
    all_candidats = get_all_candidats_enriched()
    candidats_top = sorted(all_candidats, key=lambda c: c.get('votes', 0), reverse=True)[:4]
    duels_actifs = [d for d in get_all_duels_enriched() if d and d.get('statut') == 'en_cours']

    # Calcul dynamique des statistiques
    stats = dict(STATS_GENERALES)
    stats['total_candidats'] = len(all_candidats)
    stats['total_votes'] = sum(c.get('votes', 0) for c in all_candidats)
    stats['total_duels'] = len(DUELS)
    stats['duels_en_cours'] = len(duels_actifs)
    stats['etablissements'] = len(ETABLISSEMENTS)

    contexte = {
        'candidats_top': candidats_top,
        'duels_actifs': duels_actifs,
        'stats': stats,
        'phases': PHASES,
        'categories': CATEGORIES,
        'annonces': ANNONCES,
    }
    return render(request, 'home.html', contexte)


def candidats_list(request):
    """Liste de tous les candidats inscrits."""
    contexte = {
        'candidats': get_all_candidats_enriched(),
        'categories': CATEGORIES,
    }
    return render(request, 'candidats/liste.html', contexte)


def candidat_detail(request, pk):
    """Fiche individuelle d'un candidat avec sa photo, sa vidéo et son extrait audio."""
    candidat_brut = get_candidat_by_id(pk)
    if not candidat_brut:
        raise Http404("Le profil de ce candidat est introuvable ou n'a pas encore été validé.")

    candidat = enrich_candidat(candidat_brut)

    duels_associes = [
        d for d in get_all_duels_enriched()
        if d and (d.get('candidat1_id') == pk or d.get('candidat2_id') == pk)
    ]

    contexte = {
        'candidat': candidat,
        'duels': duels_associes,
        'vote_packages': VOTES_PACKAGES,
    }
    return render(request, 'candidats/detail.html', contexte)


def duels_list(request):
    """Liste des duels de clash."""
    contexte = {
        'duels': get_all_duels_enriched(),
    }
    return render(request, 'duels/liste.html', contexte)


def duel_detail(request, pk):
    """Page face-à-face d'un duel."""
    duel = get_duel_by_id(pk)
    if not duel:
        raise Http404("Cette confrontation est introuvable.")

    contexte = {
        'duel': duel,
        'vote_packages': VOTES_PACKAGES,
    }
    return render(request, 'duels/detail.html', contexte)


def vote_page(request, candidat_id):
    """Espace de vote pour un candidat sélectionné."""
    candidat_brut = get_candidat_by_id(candidat_id)
    if not candidat_brut:
        # Si aucun candidat n'existe encore, on prépare un profil modèle vide
        candidat = {
            'id': candidat_id,
            'nom_artistique': 'En attente d\'inscription',
            'prenom': '',
            'nom': '',
            'votes': 0,
            'photo_url': '',
            'audio_titre': 'Aucun extrait déposé',
            'audio_url': '',
            'etablissement': {'nom': 'Établissement à définir'},
            'commune': '',
            'ville': 'Côte d\'Ivoire',
        }
    else:
        candidat = enrich_candidat(candidat_brut)

    contexte = {
        'candidat': candidat,
        'vote_packages': VOTES_PACKAGES,
    }
    return render(request, 'vote/index.html', contexte)


def classement(request):
    """Classement officiel (Leaderboard)."""
    tous = get_all_candidats_enriched()
    candidats_tries = sorted(tous, key=lambda c: c.get('votes', 0), reverse=True)

    contexte = {
        'candidats': candidats_tries,
        'categories': CATEGORIES,
    }
    return render(request, 'classement/index.html', contexte)


# ---------------------------------------------------------------------------
# 2. ESPACE CANDIDAT
# ---------------------------------------------------------------------------

def espace_candidat(request):
    """Tableau de bord personnel du candidat."""
    all_cands = get_all_candidats_enriched()
    candidat = all_cands[0] if all_cands else {
        'id': 0,
        'nom_artistique': 'Nouveau Candidat',
        'prenom': 'Prénom',
        'nom': 'Nom',
        'votes': 0,
        'rang': 0,
        'style': 'À définir',
        'photo_url': '',
        'etablissement': {'nom': 'Aucun établissement sélectionné'},
        'commune': '',
        'ville': '',
        'stats': {'duels_gagnes': 0, 'duels_perdus': 0, 'taux_victoire': 0},
    }

    contexte = {
        'candidat': candidat,
        'notifications': ANNONCES,
        'stats': STATS_GENERALES,
        'duels': [],
        'active_page': 'dashboard',
    }
    return render(request, 'espace_candidat/dashboard.html', contexte)


def candidat_profil(request):
    """Mise à jour du profil et photo de profil du candidat."""
    all_cands = get_all_candidats_enriched()
    candidat = all_cands[0] if all_cands else {
        'id': 0,
        'nom_artistique': '',
        'prenom': '',
        'nom': '',
        'age': '',
        'style': '',
        'bio': '',
        'photo_url': '',
        'etablissement': {'nom': ''},
        'commune': '',
        'ville': '',
    }

    contexte = {
        'candidat': candidat,
        'etablissements': ETABLISSEMENTS,
        'categories': CATEGORIES,
        'active_page': 'profil',
    }
    return render(request, 'espace_candidat/profil.html', contexte)


def candidat_medias(request):
    """Dépôt de la vidéo et de l'extrait audio du candidat."""
    all_cands = get_all_candidats_enriched()
    candidat = all_cands[0] if all_cands else {
        'id': 0,
        'nom_artistique': '',
        'audio_titre': '',
        'audio_url': '',
        'video_titre': '',
        'video_url': '',
        'video_poster': '',
    }

    contexte = {
        'candidat': candidat,
        'active_page': 'medias',
    }
    return render(request, 'espace_candidat/medias.html', contexte)


def candidat_duels_view(request):
    """Historique des confrontations du candidat."""
    contexte = {
        'candidat': get_all_candidats_enriched()[0] if get_all_candidats_enriched() else None,
        'duels': [],
        'active_page': 'duels',
    }
    return render(request, 'espace_candidat/duels.html', contexte)


def candidat_notifications(request):
    """Notifications officielles."""
    contexte = {
        'annonces': ANNONCES,
        'candidat': get_all_candidats_enriched()[0] if get_all_candidats_enriched() else None,
        'active_page': 'notifications',
    }
    return render(request, 'espace_candidat/notifications.html', contexte)


# ---------------------------------------------------------------------------
# 3. PANNEAU ADMIN
# ---------------------------------------------------------------------------

def admin_dashboard(request):
    """Vue d'ensemble de l'administration."""
    contexte = {
        'stats': STATS_GENERALES,
        'candidats': get_all_candidats_enriched(),
        'duels': get_all_duels_enriched(),
        'phases': PHASES,
        'transactions': TRANSACTIONS,
        'annonces': ANNONCES,
        'active_page': 'dashboard',
    }
    return render(request, 'admin_panel/dashboard.html', contexte)


def admin_candidats(request):
    """Gestion des candidats."""
    contexte = {
        'candidats': get_all_candidats_enriched(),
        'categories': CATEGORIES,
        'etablissements': ETABLISSEMENTS,
        'active_page': 'candidats',
    }
    return render(request, 'admin_panel/candidats.html', contexte)


def admin_votes(request):
    """Journal des votes."""
    contexte = {
        'votes': [],
        'stats': STATS_GENERALES,
        'active_page': 'votes',
    }
    return render(request, 'admin_panel/votes.html', contexte)


def admin_duels(request):
    """Gestion des duels."""
    contexte = {
        'duels': get_all_duels_enriched(),
        'phases': PHASES,
        'candidats': get_all_candidats_enriched(),
        'active_page': 'duels',
    }
    return render(request, 'admin_panel/duels.html', contexte)


def admin_transactions(request):
    """Suivi financier."""
    contexte = {
        'transactions': TRANSACTIONS,
        'vote_packages': VOTES_PACKAGES,
        'total_montant': 0,
        'active_page': 'transactions',
    }
    return render(request, 'admin_panel/transactions.html', contexte)


def admin_annonces(request):
    """Gestion des annonces."""
    contexte = {
        'annonces': ANNONCES,
        'active_page': 'annonces',
    }
    return render(request, 'admin_panel/annonces.html', contexte)


def admin_parametres(request):
    """Paramètres généraux."""
    contexte = {
        'phases': PHASES,
        'stats': STATS_GENERALES,
        'active_page': 'parametres',
    }
    return render(request, 'admin_panel/parametres.html', contexte)


# ---------------------------------------------------------------------------
# 4. AUTH
# ---------------------------------------------------------------------------

def inscription(request):
    """Inscription candidat."""
    contexte = {
        'categories': CATEGORIES,
        'etablissements': ETABLISSEMENTS,
    }
    return render(request, 'auth/inscription.html', contexte)


def connexion(request):
    """Connexion utilisateur."""
    contexte = {}
    return render(request, 'auth/connexion.html', contexte)

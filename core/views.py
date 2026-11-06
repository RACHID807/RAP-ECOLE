"""
Vues de l'application 'core'.
Chaque vue réceptionne une requête HTTP, prépare les données contextuelles
et injecte le tout dans un template HTML Django.
Les données proviennent actuellement de 'core.data' pour la phase frontend,
et seront remplacées par des requêtes de modèles (Model.objects.all(), etc.)
lors de l'implémentation du backend Django.
"""

from django.shortcuts import render
from django.http import Http404
from .data import (
    CATEGORIES, ETABLISSEMENTS, CANDIDATS, DUELS, VOTES_PACKAGES,
    ANNONCES, STATS_GENERALES, PHASES,
    get_candidat_by_id, get_duel_by_id, enrich_candidat,
    get_all_candidats_enriched, get_all_duels_enriched,
)

# ---------------------------------------------------------------------------
# TRANSACTIONS DE DÉMONSTRATION (RÉFÉRENCES OPÉRATEURS IVOIRIENS)
# Préparé pour Wave, Orange Money CI, MTN Mobile Money CI, Moov Money
# ---------------------------------------------------------------------------
TRANSACTIONS_DEMO = [
    {
        'id': 1,
        'candidat': 'Kader MC',
        'pack': 'Pack Soutien Établissement',
        'montant': 1000,
        'operateur': 'Wave Côte d\'Ivoire',
        'date': '05/11/2026 14:32',
        'statut': 'succes',
    },
    {
        'id': 2,
        'candidat': 'Aïcha La Plume',
        'pack': 'Pack Communauté',
        'montant': 2500,
        'operateur': 'Orange Money CI',
        'date': '05/11/2026 11:15',
        'statut': 'succes',
    },
    {
        'id': 3,
        'candidat': 'Yopougon Boy',
        'pack': 'Pack Découverte',
        'montant': 500,
        'operateur': 'MTN MoMo CI',
        'date': '04/11/2026 18:40',
        'statut': 'succes',
    },
    {
        'id': 4,
        'candidat': 'Junior Flow',
        'pack': 'Pack Soutien Établissement',
        'montant': 1000,
        'operateur': 'Moov Money CI',
        'date': '04/11/2026 09:20',
        'statut': 'en_attente',
    },
]

# ---------------------------------------------------------------------------
# 1. PAGES PUBLIQUES
# ---------------------------------------------------------------------------

def home(request):
    """
    Page d'accueil principale de la compétition.
    Affiche la présentation officielle, les duels actifs, le podium actuel,
    les statistiques consolidées et le calendrier des phases.
    """
    all_candidats = get_all_candidats_enriched()
    # Classement par nombre de voix décroissant
    candidats_top = sorted(all_candidats, key=lambda c: c['votes'], reverse=True)[:4]
    duels_actifs = [d for d in get_all_duels_enriched() if d and d.get('statut') == 'en_cours']

    contexte = {
        'candidats_top': candidats_top,
        'duels_actifs': duels_actifs,
        'stats': STATS_GENERALES,
        'phases': PHASES,
        'categories': CATEGORIES,
        'annonces': ANNONCES,
    }
    return render(request, 'home.html', contexte)


def candidats_list(request):
    """
    Répertoire des candidats inscrits à la compétition.
    Permet la recherche par nom et le filtrage par niveau (Collège, Lycée, Université).
    """
    contexte = {
        'candidats': get_all_candidats_enriched(),
        'categories': CATEGORIES,
    }
    return render(request, 'candidats/liste.html', contexte)


def candidat_detail(request, pk):
    """
    Fiche descriptive individuelle d'un candidat.
    Affiche l'établissement, les statistiques de vote, l'extrait audio
    et la possibilité d'apporter un soutien (gratuit ou via pack).
    """
    candidat_brut = get_candidat_by_id(pk)
    if not candidat_brut:
        raise Http404("Le profil de ce candidat est introuvable.")

    candidat = enrich_candidat(candidat_brut)

    # Récupération des confrontations auxquelles ce candidat participe
    duels_associes = [
        d for d in get_all_duels_enriched()
        if d and (d['candidat1_id'] == pk or d['candidat2_id'] == pk)
    ]

    contexte = {
        'candidat': candidat,
        'duels': duels_associes,
        'vote_packages': VOTES_PACKAGES,
    }
    return render(request, 'candidats/detail.html', contexte)


def duels_list(request):
    """
    Liste générale des confrontations (en cours et achevées).
    Met en relation les deux candidats de chaque affiche.
    """
    contexte = {
        'duels': get_all_duels_enriched(),
    }
    return render(request, 'duels/liste.html', contexte)


def duel_detail(request, pk):
    """
    Page d'un duel en face-à-face direct.
    Permet de comparer les deux participants, d'écouter leurs extraits
    et de voter en temps réel avec calcul des pourcentages.
    """
    duel = get_duel_by_id(pk)
    if not duel:
        raise Http404("Cette confrontation est introuvable.")

    contexte = {
        'duel': duel,
        'vote_packages': VOTES_PACKAGES,
    }
    return render(request, 'duels/detail.html', contexte)


def vote_page(request, candidat_id):
    """
    Page dédiée au vote pour un candidat donné.
    Propose :
      1) Un vote gratuit quotidien par écoute
      2) Un vote via packs de soutien (Mobile Money Côte d'Ivoire simulé)
    """
    candidat_brut = get_candidat_by_id(candidat_id)
    if not candidat_brut:
        raise Http404("Candidat introuvable.")

    contexte = {
        'candidat': enrich_candidat(candidat_brut),
        'vote_packages': VOTES_PACKAGES,
    }
    return render(request, 'vote/index.html', contexte)


def classement(request):
    """
    Page officielle des classements de la compétition.
    Comprend le tableau général et les filtres par catégorie scolaire.
    """
    tous = get_all_candidats_enriched()
    candidats_tries = sorted(tous, key=lambda c: c['votes'], reverse=True)

    contexte = {
        'candidats': candidats_tries,
        'categories': CATEGORIES,
    }
    return render(request, 'classement/index.html', contexte)


# ---------------------------------------------------------------------------
# 2. ESPACE PERSONNEL DU CANDIDAT (TABLEAU DE BORD)
# ---------------------------------------------------------------------------

def espace_candidat(request):
    """
    Vue d'accueil du tableau de bord d'un candidat connecté.
    Utilise le premier candidat comme profil témoin pour la démonstration.
    """
    candidat = enrich_candidat(get_candidat_by_id(1))
    contexte = {
        'candidat': candidat,
        'notifications': ANNONCES,
        'stats': STATS_GENERALES,
        'duels': [d for d in get_all_duels_enriched() if d and (d['candidat1_id'] == 1 or d['candidat2_id'] == 1)],
        'active_page': 'dashboard',
    }
    return render(request, 'espace_candidat/dashboard.html', contexte)


def candidat_profil(request):
    """Formulaire de mise à jour du profil artistique et civil du candidat."""
    contexte = {
        'candidat': enrich_candidat(get_candidat_by_id(1)),
        'etablissements': ETABLISSEMENTS,
        'categories': CATEGORIES,
        'active_page': 'profil',
    }
    return render(request, 'espace_candidat/profil.html', contexte)


def candidat_medias(request):
    """Gestion des morceaux audio, vidéos et photos déposés par le candidat."""
    medias_deposes = [
        {
            'id': 1,
            'titre': 'La Voix des Cahiers (Enregistrement studio)',
            'type': 'audio',
            'duree': '2:45',
            'date_depot': '25/10/2026',
            'statut': 'valide',
        },
        {
            'id': 2,
            'titre': 'Prestation au Lycée Classique d\'Abidjan',
            'type': 'video',
            'duree': '3:20',
            'date_depot': '29/10/2026',
            'statut': 'valide',
        },
        {
            'id': 3,
            'titre': 'Freestyle Qualification Commune',
            'type': 'audio',
            'duree': '1:50',
            'date_depot': '02/11/2026',
            'statut': 'en_revue',
        },
    ]
    contexte = {
        'candidat': enrich_candidat(get_candidat_by_id(1)),
        'medias': medias_deposes,
        'active_page': 'medias',
    }
    return render(request, 'espace_candidat/medias.html', contexte)


def candidat_duels_view(request):
    """Historique des confrontations et résultats du candidat."""
    contexte = {
        'candidat': enrich_candidat(get_candidat_by_id(1)),
        'duels': [d for d in get_all_duels_enriched() if d and (d['candidat1_id'] == 1 or d['candidat2_id'] == 1)],
        'active_page': 'duels',
    }
    return render(request, 'espace_candidat/duels.html', contexte)


def candidat_notifications(request):
    """Boîte de réception des messages et annonces officielles adressées au candidat."""
    contexte = {
        'candidat': enrich_candidat(get_candidat_by_id(1)),
        'annonces': ANNONCES,
        'active_page': 'notifications',
    }
    return render(request, 'espace_candidat/notifications.html', contexte)


# ---------------------------------------------------------------------------
# 3. PANNEAU D'ADMINISTRATION
# ---------------------------------------------------------------------------

def admin_dashboard(request):
    """
    Vue de synthèse pour les organisateurs de la compétition :
    chiffres globaux, progression des votes, inscriptions et calendrier.
    """
    contexte = {
        'stats': STATS_GENERALES,
        'candidats': get_all_candidats_enriched(),
        'duels': get_all_duels_enriched(),
        'phases': PHASES,
        'transactions': TRANSACTIONS_DEMO,
        'annonces': ANNONCES,
        'active_page': 'dashboard',
    }
    return render(request, 'admin_panel/dashboard.html', contexte)


def admin_candidats(request):
    """Gestion des fiches candidats, validation et modification des dossiers."""
    contexte = {
        'candidats': get_all_candidats_enriched(),
        'categories': CATEGORIES,
        'etablissements': ETABLISSEMENTS,
        'active_page': 'candidats',
    }
    return render(request, 'admin_panel/candidats.html', contexte)


def admin_votes(request):
    """Journal de contrôle des votes enregistrés sur la plateforme."""
    journal_votes = [
        {'id': 101, 'electeur': 'Citoyen_Abidjan_01', 'candidat': 'Kader MC', 'type': 'gratuit', 'date': '05/11/2026 14:40', 'commune': 'Cocody'},
        {'id': 102, 'electeur': 'Citoyen_Abidjan_02', 'candidat': 'Aïcha La Plume', 'type': 'pack', 'date': '05/11/2026 14:35', 'commune': 'Cocody'},
        {'id': 103, 'electeur': 'Citoyen_Yopougon_01', 'candidat': 'Yopougon Boy', 'type': 'gratuit', 'date': '05/11/2026 14:22', 'commune': 'Yopougon'},
        {'id': 104, 'electeur': 'Citoyen_Plateau_01', 'candidat': 'Junior Flow', 'type': 'gratuit', 'date': '05/11/2026 14:10', 'commune': 'Plateau'},
        {'id': 105, 'electeur': 'Citoyen_Yakro_01', 'candidat': 'Bélier du Centre', 'type': 'pack', 'date': '05/11/2026 13:50', 'commune': 'Yamoussoukro'},
    ]
    contexte = {
        'votes': journal_votes,
        'stats': STATS_GENERALES,
        'active_page': 'votes',
    }
    return render(request, 'admin_panel/votes.html', contexte)


def admin_duels(request):
    """Programmation des rencontres, affectation des étapes et des jurys."""
    contexte = {
        'duels': get_all_duels_enriched(),
        'phases': PHASES,
        'candidats': get_all_candidats_enriched(),
        'active_page': 'duels',
    }
    return render(request, 'admin_panel/duels.html', contexte)


def admin_transactions(request):
    """Suivi comptable des contributions de soutien par opérateur (Wave, Orange, MTN, Moov)."""
    contexte = {
        'transactions': TRANSACTIONS_DEMO,
        'vote_packages': VOTES_PACKAGES,
        'total_montant': sum(t['montant'] for t in TRANSACTIONS_DEMO if t['statut'] == 'succes'),
        'active_page': 'transactions',
    }
    return render(request, 'admin_panel/transactions.html', contexte)


def admin_annonces(request):
    """Publication des communiqués et informations officielles pour les participants."""
    contexte = {
        'annonces': ANNONCES,
        'active_page': 'annonces',
    }
    return render(request, 'admin_panel/annonces.html', contexte)


def admin_parametres(request):
    """Configuration générale des dates, des règles de vote et des coefficients."""
    contexte = {
        'phases': PHASES,
        'stats': STATS_GENERALES,
        'active_page': 'parametres',
    }
    return render(request, 'admin_panel/parametres.html', contexte)


# ---------------------------------------------------------------------------
# 4. AUTHENTIFICATION ET CANDIDATURE
# ---------------------------------------------------------------------------

def inscription(request):
    """Dépôt de candidature d'un nouvel élève ou étudiant."""
    contexte = {
        'categories': CATEGORIES,
        'etablissements': ETABLISSEMENTS,
    }
    return render(request, 'auth/inscription.html', contexte)


def connexion(request):
    """Interface de connexion pour les candidats et organisateurs."""
    contexte = {}
    return render(request, 'auth/connexion.html', contexte)

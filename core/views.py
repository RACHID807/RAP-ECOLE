"""
Vues de l'application 'core'.
Toutes les données fictives ont été retirées.
Les vues transmettent les données de la base (actuellement vides)
et gèrent proprement les cas où aucun candidat ou duel n'est encore enregistré.
"""

from functools import wraps
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from django.contrib import messages
from .data import (
    CATEGORIES, ETABLISSEMENTS, CANDIDATS, DUELS, VOTES_PACKAGES,
    ANNONCES, STATS_GENERALES, PHASES, WAVE_PAY_URL, MESSAGE_DEFILANT, WHATSAPP_URL,
    VOTES, TRANSACTIONS,
    get_candidat_by_id, get_duel_by_id, enrich_candidat,
    get_all_candidats_enriched, get_all_duels_enriched,
    ajouter_vote, valider_vote_admin, get_all_votes, get_vote_by_id,
)
from .brevo_service import envoyer_confirmation_vote_brevo

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
    """
    Espace de vote pour un candidat sélectionné.
    Gère la sélection du pack Wave à 500 FCFA, la saisie des coordonnées de paiement,
    et la transmission du vote en attente de vérification administrative.
    """
    candidat_brut = get_candidat_by_id(candidat_id)
    if not candidat_brut:
        candidat = {
            'id': candidat_id,
            'nom_artistique': f"Candidat #{candidat_id}",
            'prenom': '',
            'nom': '',
            'votes': 0,
            'photo_url': '',
            'audio_titre': 'Extrait en cours de traitement',
            'audio_url': '',
            'etablissement': {'nom': 'Établissement scolaire / universitaire'},
            'commune': 'Abidjan',
            'ville': 'Côte d\'Ivoire',
        }
    else:
        candidat = enrich_candidat(candidat_brut)

    vote_enregistre = None
    erreur_vote = None

    if request.method == 'POST':
        votant_nom = request.POST.get('votant_nom', '').strip()
        votant_email = request.POST.get('votant_email', '').strip()
        votant_telephone = request.POST.get('votant_telephone', '').strip()
        package_id = request.POST.get('package_id', 'pass_solo')

        # Trouver le pack choisi
        pack_choisi = next((p for p in VOTES_PACKAGES if p['id'] == package_id), VOTES_PACKAGES[0])
        montant = pack_choisi['prix']
        voix = pack_choisi['votes']

        if not votant_telephone:
            erreur_vote = "Veuillez indiquer le numéro de téléphone utilisé pour le paiement Wave."
        elif not votant_email:
            erreur_vote = "Veuillez renseigner votre adresse courriel pour recevoir la confirmation Brevo."
        else:
            vote_enregistre = ajouter_vote(
                votant_nom=votant_nom or "Supporter anonyme",
                votant_email=votant_email,
                votant_telephone=votant_telephone,
                candidat_id=candidat_id,
                montant=montant,
                nb_voix=voix,
                methode='Wave CI'
            )

    contexte = {
        'candidat': candidat,
        'vote_packages': VOTES_PACKAGES,
        'wave_pay_url': WAVE_PAY_URL,
        'vote_enregistre': vote_enregistre,
        'erreur_vote': erreur_vote,
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


# Mot de passe secret pour l'accès au panneau d'administration
ADMIN_PASSWORD = 'adminrap_ec@le'


def admin_required(view_func):
    """
    Décorateur de sécurité pour l'espace administration.
    Vérifie si la session en cours a validé le mot de passe 'adminrap_ec@le'.
    Redirige vers l'écran de connexion admin si non authentifié.
    """
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            return redirect(f"{reverse('admin_login')}?next={request.path}")
        return view_func(request, *args, **kwargs)
    return _wrapped


# ---------------------------------------------------------------------------
# 3. PANNEAU ADMIN (ACCÈS SÉCURISÉ)
# ---------------------------------------------------------------------------

def admin_login(request):
    """
    Page d'authentification pour le comité d'organisation.
    Vérifie la conformité du mot de passe 'adminrap_ec@le'.
    """
    # Si déjà connecté, rediriger directement vers le dashboard
    if request.session.get('admin_logged_in'):
        return redirect('admin_dashboard')

    erreur = None
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('admin_dashboard')

    if request.method == 'POST':
        mot_de_passe = request.POST.get('mot_de_passe', '').strip()
        if mot_de_passe == ADMIN_PASSWORD:
            request.session['admin_logged_in'] = True
            return redirect(next_url)
        else:
            erreur = "Mot de passe administrateur incorrect. Veuillez vérifier votre saisie."

    contexte = {
        'erreur': erreur,
        'next_url': next_url,
    }
    return render(request, 'admin_panel/login.html', contexte)


def admin_logout(request):
    """
    Déconnexion sécurisée de la session administrateur.
    """
    if 'admin_logged_in' in request.session:
        del request.session['admin_logged_in']
    return redirect('admin_login')


@admin_required
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


@admin_required
def admin_candidats(request):
    """Gestion des candidats."""
    contexte = {
        'candidats': get_all_candidats_enriched(),
        'categories': CATEGORIES,
        'etablissements': ETABLISSEMENTS,
        'active_page': 'candidats',
    }
    return render(request, 'admin_panel/candidats.html', contexte)


@admin_required
def admin_votes(request):
    """
    Journal de contrôle et de validation des votes par l'administration.
    Permet de vérifier le numéro Wave et l'heure exacte du paiement
    avant de valider le vote et d'envoyer l'email Brevo.
    """
    message_succes = request.GET.get('succes')
    contexte = {
        'votes': get_all_votes(),
        'stats': STATS_GENERALES,
        'message_succes': message_succes,
        'active_page': 'votes',
    }
    return render(request, 'admin_panel/votes.html', contexte)


@admin_required
def admin_valider_vote(request, vote_id):
    """
    Action administrateur : validation d'un vote après pointage du paiement Wave.
    Incrémente les voix du candidat, met à jour les transactions et envoie
    automatiquement le courriel de confirmation au votant via Brevo.
    """
    vote = get_vote_by_id(vote_id)
    if not vote:
        raise Http404("Vote introuvable.")

    succes, msg = valider_vote_admin(vote_id)

    if succes:
        # Envoi de la notification courriel via Brevo
        email_ok, email_msg = envoyer_confirmation_vote_brevo(
            votant_nom=vote.get('votant_nom'),
            votant_email=vote.get('votant_email'),
            candidat_nom=vote.get('candidat_nom'),
            nb_voix=vote.get('voix', 1),
            montant=vote.get('montant', 500),
            telephone=vote.get('votant_telephone'),
        )
        vote['email_envoye'] = email_ok
        vote['email_msg'] = email_msg
        texte_retour = f"Le vote #{vote_id} de {vote.get('votant_nom')} (+{vote.get('voix')} voix) a été validé ! {email_msg}"
    else:
        texte_retour = msg

    return redirect(f"{reverse('admin_votes')}?succes={texte_retour}")


@admin_required
def admin_duels(request):
    """Gestion des duels."""
    contexte = {
        'duels': get_all_duels_enriched(),
        'phases': PHASES,
        'candidats': get_all_candidats_enriched(),
        'active_page': 'duels',
    }
    return render(request, 'admin_panel/duels.html', contexte)


@admin_required
def admin_transactions(request):
    """Suivi financier."""
    contexte = {
        'transactions': TRANSACTIONS,
        'vote_packages': VOTES_PACKAGES,
        'total_montant': 0,
        'active_page': 'transactions',
    }
    return render(request, 'admin_panel/transactions.html', contexte)


@admin_required
def admin_annonces(request):
    """Gestion des annonces."""
    contexte = {
        'annonces': ANNONCES,
        'active_page': 'annonces',
    }
    return render(request, 'admin_panel/annonces.html', contexte)


@admin_required
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

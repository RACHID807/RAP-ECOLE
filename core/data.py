"""
Structure de données du projet RAP CLASH SCHOOL (RCS).
Toutes les données fictives (faux candidats, faux votes, faux duels, faux chiffres)
ont été vidées. Les listes sont prêtes à être alimentées par la base de données Django
(modèles Candidat, Duel, Etablissement, Vote, etc.).
"""

# Catégories de base du système scolaire (niveaux officiels)
CATEGORIES = [
    {
        'id': 1,
        'nom': 'Collège',
        'slug': 'college',
        'description': '6ème à la 3ème',
    },
    {
        'id': 2,
        'nom': 'Lycée',
        'slug': 'lycee',
        'description': '2nde à la Terminale',
    },
    {
        'id': 3,
        'nom': 'Université & Grandes Écoles',
        'slug': 'universite',
        'description': 'Enseignement Supérieur',
    },
]

# ---------------------------------------------------------------------------
# 2. ÉTABLISSEMENTS SCOLAIRES ET UNIVERSITAIRES (CÔTE D'IVOIRE)
# ---------------------------------------------------------------------------
ETABLISSEMENTS = [
    {
        'id': 1,
        'nom': 'Lycée Classique d\'Abidjan (LCA)',
        'commune': 'Cocody',
        'ville': 'Abidjan',
        'categorie_id': 2,
    },
    {
        'id': 2,
        'nom': 'Lycée Moderne de Cocody (LMC)',
        'commune': 'Cocody',
        'ville': 'Abidjan',
        'categorie_id': 2,
    },
    {
        'id': 3,
        'nom': 'Lycée Municipal d\'Attécoubé',
        'commune': 'Attécoubé',
        'ville': 'Abidjan',
        'categorie_id': 2,
    },
    {
        'id': 4,
        'nom': 'Collège Moderne du Plateau',
        'commune': 'Plateau',
        'ville': 'Abidjan',
        'categorie_id': 1,
    },
    {
        'id': 5,
        'nom': 'Collège Rodin Yopougon',
        'commune': 'Yopougon',
        'ville': 'Abidjan',
        'categorie_id': 1,
    },
    {
        'id': 6,
        'nom': 'Université Félix Houphouët-Boigny (UFHB)',
        'commune': 'Cocody',
        'ville': 'Abidjan',
        'categorie_id': 3,
    },
    {
        'id': 7,
        'nom': 'Université Nangui Abrogoua (UNA)',
        'commune': 'Abobo',
        'ville': 'Abidjan',
        'categorie_id': 3,
    },
    {
        'id': 8,
        'nom': 'Institut National Polytechnique Félix Houphouët-Boigny (INP-HB)',
        'commune': 'Yamoussoukro',
        'ville': 'Yamoussoukro',
        'categorie_id': 3,
    },
    {
        'id': 9,
        'nom': "Ecole Multinationale Superieure des Postes d'Abidjan (EMSP)",
        'commune': 'Treichville',
        'ville': 'Abidjan',
        'categorie_id': 3,
    },
    {
        'id': 10,
        'nom': "Lycée Moderne de Cocody Angre (LMCA)",
        'commune': 'Cocody',
        'ville': 'Abidjan',
        'categorie_id': 2,
    },
    {
        'id': 11,
        'nom': "Collège Anador Abobo",
        'commune': 'Abobo',
        'ville': 'Abidjan',
        'categorie_id': 1,
    },
    {
        'id': 12,
        'nom': 'Lycée Moderne de Treichville',
        'commune': 'Attécoubé',
        'ville': 'Abidjan',
        'categorie_id': 2,
    },
    {
        'id': 13,
        'nom': 'Collège Nanti Abobo',
        'commune': 'Abobo',
        'ville': 'Abidjan',
        'categorie_id': 1,
    },
    {
        'id': 14,
        'nom': 'Collège Privé Averroes',
        'commune': 'Abobo',
        'ville': 'Abidjan',
        'categorie_id': 1,
    },
    {
        'id': 15,
        'nom': 'Collège Sainte-Jeanne Abobo',
        'commune': 'Abobo',
        'ville': 'Abidjan',
        'categorie_id': 1,
    },
    {
        'id': 16,
        'nom': 'Ecole Superieure Africaine de la technologie, de l\'information et de la communication (ESATIC)',
        'commune': 'Treichville',
        'ville': 'Abidjan',
        'categorie_id': 3,
    },

]

# Liste des candidats (vide jusqu'à inscription)
CANDIDATS = []

# Liste des duels / confrontations (vide jusqu'à programmation)
DUELS = []

# Lien officiel Wave CI pour les votes
WAVE_PAY_URL = "https://pay.wave.com/m/M_ci_oFeZQRw9aDIm/c/ci/"

# Message défilant officiel (modifiable)
MESSAGE_DEFILANT = "information : bienvenue sur RAP CLASH SCHOOL , A Bientot pour les duels ."

# Lien officiel WhatsApp Côte d'Ivoire (Numéro officiel du comité : +225 07 57 33 30 78)
WHATSAPP_URL = "https://wa.me/2250757333078?text=Bonjour%20RAP%20CLASH%20SCHOOL%20CI"

# Formules de Vote officielles - Prix de base 500 FCFA avec Wave direct
VOTES_PACKAGES = [
    {
        'id': 'pass_solo',
        'nom': 'Vote Solo Wave',
        'prix': 500,
        'devise': 'FCFA',
        'votes': 1,
        'couleur': '#00E5FF',
        'populaire': True,
        'avantages': ['1 vote officiel comptabilisé', 'Paiement Wave direct à 500 FCFA', 'Confirmation certifiée par email Brevo'],
    },
    {
        'id': 'pass_force',
        'nom': 'Vote Force (Pack 5)',
        'prix': 2500,
        'devise': 'FCFA',
        'votes': 5,
        'couleur': '#FF6B00',
        'avantages': ['5 votes crédités directement', 'Paiement Wave à 2 500 FCFA', 'Mise en avant du votant'],
    },
    {
        'id': 'pass_choc',
        'nom': 'Vote Maxi Clash (Pack 10)',
        'prix': 5000,
        'devise': 'FCFA',
        'votes': 10,
        'couleur': '#FFC107',
        'avantages': ['10 votes d\'encouragement', 'Paiement Wave à 5 000 FCFA', 'Badge Super Supporter'],
    },
]

# Liste des votes soumis (en attente ou validés par l'administration)
VOTES = []

# Liste des transactions validées
TRANSACTIONS = []

# Annonces officielles
ANNONCES = []

# Phases du calendrier
PHASES = [
    {'id': 1, 'nom': 'Inscriptions & Dépôt des Médias', 'statut': 'en_cours', 'date': 'En cours'},
    {'id': 2, 'nom': 'Sélection des Candidats', 'statut': 'a_venir', 'date': 'À venir'},
    {'id': 3, 'nom': 'Quarts de Finale', 'statut': 'a_venir', 'date': 'À venir'},
    {'id': 4, 'nom': 'Demi-Finales Live', 'statut': 'a_venir', 'date': 'À venir'},
    {'id': 5, 'nom': 'Grande Finale Abidjan', 'statut': 'a_venir', 'date': 'À venir'},
]

# Statistiques réelles (initialisées à zéro)
STATS_GENERALES = {
    'total_candidats': 0,
    'total_votes': 0,
    'votes_premium': 0,
    'total_duels': 0,
    'duels_en_cours': 0,
    'etablissements': 0,
    'categories': 3,
    'montant_transactions': 0,
}


def get_candidat_by_id(candidat_id):
    """Recherche un candidat par son identifiant."""
    for c in CANDIDATS:
        if c.get('id') == candidat_id:
            return c
    return None


def get_etablissement_by_id(etab_id):
    """Recherche un établissement par son identifiant."""
    for e in ETABLISSEMENTS:
        if e.get('id') == etab_id:
            return e
    return None


def get_categorie_by_id(cat_id):
    """Recherche une catégorie par son identifiant."""
    for c in CATEGORIES:
        if c.get('id') == cat_id:
            return c
    return None


def enrich_candidat(candidat):
    """Associe la catégorie et l'établissement au candidat."""
    if not candidat:
        return None
    c = dict(candidat)
    c['etablissement'] = get_etablissement_by_id(c.get('etablissement_id'))
    c['categorie'] = get_categorie_by_id(c.get('categorie_id'))
    return c


def get_all_candidats_enriched():
    """Retourne la liste des candidats inscrits."""
    return [enrich_candidat(c) for c in CANDIDATS]


def get_duel_by_id(duel_id):
    """Retourne les informations d'un duel."""
    for d in DUELS:
        if d.get('id') == duel_id:
            d_copy = dict(d)
            d_copy['candidat1'] = enrich_candidat(get_candidat_by_id(d.get('candidat1_id')))
            d_copy['candidat2'] = enrich_candidat(get_candidat_by_id(d.get('candidat2_id')))
            total = d.get('votes1', 0) + d.get('votes2', 0)
            d_copy['pct1'] = round((d.get('votes1', 0) / total) * 100) if total > 0 else 50
            d_copy['pct2'] = round((d.get('votes2', 0) / total) * 100) if total > 0 else 50
            return d_copy
    return None


def get_all_duels_enriched():
    """Retourne la liste de tous les duels."""
    return [get_duel_by_id(d['id']) for d in DUELS if 'id' in d]


def get_all_votes():
    """Retourne l'ensemble des votes enregistrés (triés par date décroissante)."""
    return sorted(VOTES, key=lambda v: v.get('id', 0), reverse=True)


def get_vote_by_id(vote_id):
    """Recherche un vote par son identifiant unique."""
    for v in VOTES:
        if v.get('id') == vote_id:
            return v
    return None


def ajouter_vote(votant_nom, votant_email, votant_telephone, candidat_id, montant=500, nb_voix=1, methode='Wave CI'):
    """Enregistre une nouvelle demande de vote soumise par un internaute."""
    candidat = get_candidat_by_id(candidat_id)
    candidat_nom = candidat.get('nom_artistique') if candidat else f"Candidat #{candidat_id}"

    from datetime import datetime
    maintenant = datetime.now()

    vote_id = (VOTES[-1]['id'] + 1) if VOTES else 1
    nouveau_vote = {
        'id': vote_id,
        'votant_nom': votant_nom.strip() or "Supporter Anonyme",
        'votant_email': votant_email.strip(),
        'votant_telephone': votant_telephone.strip(),
        'candidat_id': candidat_id,
        'candidat_nom': candidat_nom,
        'montant': montant,
        'voix': nb_voix,
        'methode': methode,
        'statut': 'en_attente',  # 'en_attente' ou 'valide'
        'date_heure': maintenant.strftime("%d/%m/%Y à %H:%M:%S"),
        'heure_precise': maintenant.strftime("%H:%M:%S"),
        'date_validation': None,
        'email_envoye': False,
    }
    VOTES.append(nouveau_vote)

    # Persistance automatique dans la base de données
    try:
        from .db_service import sauvegarder_vote_db
        sauvegarder_vote_db(
            votant_nom=nouveau_vote['votant_nom'],
            votant_email=nouveau_vote['votant_email'],
            votant_telephone=nouveau_vote['votant_telephone'],
            candidat_id=candidat_id,
            montant=montant,
            nb_voix=nb_voix,
            methode=methode
        )
    except Exception as e:
        print(f"[DB LOG] Synchronisation Vote DB : {e}")

    return nouveau_vote


def valider_vote_admin(vote_id):
    """
    Validation administrative du vote après vérification de l'heure et du numéro Wave.
    Incrémente les voix du candidat, met à jour les stats et enregistre la transaction.
    """
    vote = get_vote_by_id(vote_id)
    if not vote:
        return False, "Vote introuvable."

    if vote.get('statut') == 'valide':
        return False, "Ce vote a déjà été validé."

    from datetime import datetime
    maintenant = datetime.now().strftime("%d/%m/%Y à %H:%M:%S")

    # Mise à jour du vote
    vote['statut'] = 'valide'
    vote['date_validation'] = maintenant

    # Crédit des voix au candidat
    candidat = get_candidat_by_id(vote['candidat_id'])
    if candidat:
        candidat['votes'] = candidat.get('votes', 0) + vote.get('voix', 1)

    # Mise à jour des statistiques globales
    STATS_GENERALES['total_votes'] = STATS_GENERALES.get('total_votes', 0) + vote.get('voix', 1)
    STATS_GENERALES['votes_premium'] = STATS_GENERALES.get('votes_premium', 0) + vote.get('voix', 1)
    STATS_GENERALES['montant_transactions'] = STATS_GENERALES.get('montant_transactions', 0) + vote.get('montant', 500)

    # Enregistrement de la transaction financière
    transac_id = (TRANSACTIONS[-1]['id'] + 1) if TRANSACTIONS else 1
    TRANSACTIONS.append({
        'id': transac_id,
        'reference': f"WAVE-{vote['id']:04d}-{vote['votant_telephone'][-4:] if len(vote['votant_telephone'])>=4 else '0000'}",
        'candidat': vote['candidat_nom'],
        'operateur': 'Wave CI',
        'telephone': vote['votant_telephone'],
        'montant': vote['montant'],
        'date': maintenant,
        'vote_id': vote['id'],
    })

    # Persistance de la validation en base de données
    try:
        from .db_service import valider_vote_db
        valider_vote_db(vote_id)
    except Exception as e:
        print(f"[DB LOG] Validation Vote DB : {e}")

    return True, "Vote validé avec succès."


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

# Liste des établissements inscrits (vide jusqu'à inscription)
ETABLISSEMENTS = []

# Liste des candidats (vide jusqu'à inscription)
CANDIDATS = []

# Liste des duels / confrontations (vide jusqu'à programmation)
DUELS = []

# Formules de Vote Pass officielles pour Wave, Djamo et Orange Money
VOTES_PACKAGES = [
    {
        'id': 'pass_starter',
        'nom': 'Vote Pass Starter',
        'prix': 500,
        'devise': 'FCFA',
        'votes': 10,
        'couleur': '#FF6B00',
        'avantages': ['10 votes instantanés', 'Paiement Wave / Djamo / Orange Money'],
    },
    {
        'id': 'pass_vip',
        'nom': 'Vote Pass VIP',
        'prix': 2000,
        'devise': 'FCFA',
        'votes': 50,
        'couleur': '#FFC107',
        'populaire': True,
        'avantages': ['50 votes instantanés', 'Badge VIP sur le profil'],
    },
    {
        'id': 'pass_champion',
        'nom': 'Vote Pass Champion',
        'prix': 5000,
        'devise': 'FCFA',
        'votes': 150,
        'couleur': '#00E676',
        'avantages': ['150 votes massifs', 'Mise en avant sur l\'écran live'],
    },
]

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

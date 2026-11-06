"""
Module de données et structures de référence pour le projet RAP ÉCOLE.
Ce fichier sert de contrat de données pour l'équipe (frontend & futur backend Django).
Toutes les entités reflètent le contexte ivoirien (établissements et communes de Côte d'Ivoire).
Lors du branchement avec Django ORM / Django REST Framework, ces listes seront remplacées
par les requêtes de modèles réels (ex: Candidat.objects.filter(statut='actif')).
"""

# ---------------------------------------------------------------------------
# 1. CATÉGORIES SCOLAIRES ET UNIVERSITAIRES
# ---------------------------------------------------------------------------
CATEGORIES = [
    {
        'id': 1,
        'nom': 'Collège',
        'slug': 'college',
        'description': 'Élèves du premier cycle de l\'enseignement secondaire (6ème à 3ème)',
    },
    {
        'id': 2,
        'nom': 'Lycée',
        'slug': 'lycee',
        'description': 'Élèves du second cycle de l\'enseignement secondaire (2nde à Terminale)',
    },
    {
        'id': 3,
        'nom': 'Université & Grandes Écoles',
        'slug': 'universite',
        'description': 'Étudiants des universités publiques, privées et instituts supérieurs',
    },
]

# ---------------------------------------------------------------------------
# 2. ÉTABLISSEMENTS SCOLAIRES ET UNIVERSITAIRES (CÔTE D'IVOIRE)
# ---------------------------------------------------------------------------
ETABLISSEMENTS = [
    {
        'id': 1,
        'nom': 'Lycée Classique d\'Abidjan',
        'commune': 'Cocody',
        'ville': 'Abidjan',
        'categorie_id': 2,
    },
    {
        'id': 2,
        'nom': 'Lycée Moderne de Cocody',
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
        'nom': 'Collège d\'Enseignement Général de Yopougon',
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
]

# ---------------------------------------------------------------------------
# 3. CANDIDATS (Profils réels ivoiriens sans avatars fantaisistes)
# Les photos sont gérées de manière sobre via des placeholders d'images réelles
# ou des photos professionnelles fournies par les candidats.
# ---------------------------------------------------------------------------
CANDIDATS = [
    {
        'id': 1,
        'nom_artistique': 'Kader MC',
        'prenom': 'Abdoulaye',
        'nom': 'Koné',
        'bio': "Passionné de lyricisme et de rap conscient depuis le collège. Il aborde les réalités scolaires, le travail et la persévérance de la jeunesse ivoirienne.",
        'etablissement_id': 1,
        'categorie_id': 2,
        'votes': 1420,
        'rang': 1,
        'statut': 'actif',
        'commune': 'Cocody',
        'ville': 'Abidjan',
        'style': 'Rap conscient',
        'age': 17,
        'photo_url': '',  # Champ prévu pour le futur téléversement d'image réelle
        'audio_titre': 'La Voix des Cahiers',
        'stats': {
            'duels_gagnes': 4,
            'duels_perdus': 0,
            'taux_victoire': 100,
        },
    },
    {
        'id': 2,
        'nom_artistique': 'Aïcha La Plume',
        'prenom': 'Aïssata',
        'nom': 'Traoré',
        'bio': "Étudiante en communication à l'UFHB. Elle mêle des rimes précises à un débit percutant inspiré de la tradition oratoire et du rap engagé.",
        'etablissement_id': 6,
        'categorie_id': 3,
        'votes': 1350,
        'rang': 2,
        'statut': 'actif',
        'commune': 'Cocody',
        'ville': 'Abidjan',
        'style': 'Poésie & Rap',
        'age': 20,
        'photo_url': '',
        'audio_titre': 'Lumière d\'Éburnie',
        'stats': {
            'duels_gagnes': 3,
            'duels_perdus': 1,
            'taux_victoire': 75,
        },
    },
    {
        'id': 3,
        'nom_artistique': 'Yopougon Boy',
        'prenom': 'Jean-Marc',
        'nom': 'Kouassi',
        'bio': "Représentant fier de la commune de Yopougon, il apporte une énergie authentique et un flow direct qui parle à la jeunesse des quartiers populaires.",
        'etablissement_id': 3,
        'categorie_id': 2,
        'votes': 1180,
        'rang': 3,
        'statut': 'actif',
        'commune': 'Yopougon',
        'ville': 'Abidjan',
        'style': 'Street Rap',
        'age': 18,
        'photo_url': '',
        'audio_titre': 'Rue Princesse Acoustique',
        'stats': {
            'duels_gagnes': 3,
            'duels_perdus': 1,
            'taux_victoire': 75,
        },
    },
    {
        'id': 4,
        'nom_artistique': 'Junior Flow',
        'prenom': 'Moïse',
        'nom': 'Bamba',
        'bio': "Le plus jeune participant de sa section. Élève studieux au Collège Moderne du Plateau, il impressionne par sa technique d'écriture et sa maturité.",
        'etablissement_id': 4,
        'categorie_id': 1,
        'votes': 980,
        'rang': 4,
        'statut': 'actif',
        'commune': 'Plateau',
        'ville': 'Abidjan',
        'style': 'Rap classique',
        'age': 14,
        'photo_url': '',
        'audio_titre': 'Premier Tableau',
        'stats': {
            'duels_gagnes': 2,
            'duels_perdus': 1,
            'taux_victoire': 66,
        },
    },
    {
        'id': 5,
        'nom_artistique': 'Bélier du Centre',
        'prenom': 'Serge',
        'nom': 'N\'Guessan',
        'bio': "Élève-ingénieur à l'INP-HB de Yamoussoukro. Il allie rigueur scientifique et finesse littéraire dans des morceaux rythmés et structurés.",
        'etablissement_id': 8,
        'categorie_id': 3,
        'votes': 890,
        'rang': 5,
        'statut': 'actif',
        'commune': 'Yamoussoukro',
        'ville': 'Yamoussoukro',
        'style': 'Rap conceptuel',
        'age': 21,
        'photo_url': '',
        'audio_titre': 'Théorème du Rythme',
        'stats': {
            'duels_gagnes': 2,
            'duels_perdus': 2,
            'taux_victoire': 50,
        },
    },
    {
        'id': 6,
        'nom_artistique': 'Sarah Rimera',
        'prenom': 'Sarah',
        'nom': 'Koffi',
        'bio': "Collégienne originaire de Yopougon. Ses textes encouragent les jeunes filles à poursuivre leurs études et à s'exprimer par l'art.",
        'etablissement_id': 5,
        'categorie_id': 1,
        'votes': 810,
        'rang': 6,
        'statut': 'actif',
        'commune': 'Yopougon',
        'ville': 'Abidjan',
        'style': 'Slam & Rap',
        'age': 15,
        'photo_url': '',
        'audio_titre': 'Voix des Filles',
        'stats': {
            'duels_gagnes': 1,
            'duels_perdus': 2,
            'taux_victoire': 33,
        },
    },
]

# ---------------------------------------------------------------------------
# 4. DUELS / CONFRONTATIONS EN COURS
# Structure prête pour la future table 'core_duel'
# ---------------------------------------------------------------------------
DUELS = [
    {
        'id': 1,
        'candidat1_id': 1,
        'candidat2_id': 2,
        'titre': 'Confrontation Demi-Finale 1 — Kader MC vs Aïcha La Plume',
        'phase': 'Demi-finale',
        'statut': 'en_cours',
        'votes1': 1420,
        'votes2': 1350,
        'date_debut': '2026-11-01',
        'date_fin': '2026-11-15',
        'temps_restant': '6 jours',
        'description': 'Affrontement entre le Lycée Classique d\'Abidjan et l\'Université Félix Houphouët-Boigny.',
    },
    {
        'id': 2,
        'candidat1_id': 3,
        'candidat2_id': 4,
        'titre': 'Confrontation Demi-Finale 2 — Yopougon Boy vs Junior Flow',
        'phase': 'Demi-finale',
        'statut': 'en_cours',
        'votes1': 1180,
        'votes2': 980,
        'date_debut': '2026-11-01',
        'date_fin': '2026-11-15',
        'temps_restant': '6 jours',
        'description': 'Affrontement entre le Lycée Municipal d\'Attécoubé et le Collège Moderne du Plateau.',
    },
    {
        'id': 3,
        'candidat1_id': 5,
        'candidat2_id': 6,
        'titre': 'Quart de Finale — Bélier du Centre vs Sarah Rimera',
        'phase': 'Quart de finale',
        'statut': 'termine',
        'votes1': 890,
        'votes2': 810,
        'date_debut': '2026-10-20',
        'date_fin': '2026-10-30',
        'temps_restant': 'Terminé',
        'gagnant_id': 5,
        'description': 'Rencontre validée le 30 octobre 2026.',
    },
]

# ---------------------------------------------------------------------------
# 5. PACKS DE SOUTIEN (Tarification en Francs CFA standard en Côte d'Ivoire)
# Prévus pour être connectés à des passerelles locales (Wave, Orange Money, MTN MoMo, Moov)
# ---------------------------------------------------------------------------
VOTES_PACKAGES = [
    {
        'id': 'pack_decouverte',
        'nom': 'Pack Découverte',
        'prix': 500,
        'devise': 'FCFA',
        'votes': 5,
        'avantages': [
            '5 voix attribuées au candidat',
            'Reçu de contribution numérique',
        ],
    },
    {
        'id': 'pack_soutien',
        'nom': 'Pack Soutien Établissement',
        'prix': 1000,
        'devise': 'FCFA',
        'votes': 12,
        'populaire': True,
        'avantages': [
            '12 voix attribuées au candidat',
            'Soutien direct à l\'équipe de l\'établissement',
            'Notification envoyée sur la page du candidat',
        ],
    },
    {
        'id': 'pack_communaute',
        'nom': 'Pack Communauté',
        'prix': 2500,
        'devise': 'FCFA',
        'votes': 35,
        'avantages': [
            '35 voix attribuées au candidat',
            'Contribution majeure au classement',
            'Affichage du soutien dans les statistiques',
        ],
    },
    {
        'id': 'pack_majeur',
        'nom': 'Pack Partenaire Majeur',
        'prix': 5000,
        'devise': 'FCFA',
        'votes': 80,
        'avantages': [
            '80 voix attribuées au candidat',
            'Impact déterminant pour les phases finales',
            'Attestation numérique de contributeur officiel',
        ],
    },
]

# ---------------------------------------------------------------------------
# 6. ANNONCES ET COMMUNICATIONS OFFICIELLES
# ---------------------------------------------------------------------------
ANNONCES = [
    {
        'id': 1,
        'titre': 'Lancement officiel des demi-finales à Abidjan',
        'type': 'important',
        'contenu': 'Les votes pour les demi-finales sont ouverts. Vous pouvez voter pour les représentants des établissements d\'Abidjan et de Yamoussoukro.',
        'date': '01 Nov 2026',
        'lu': False,
    },
    {
        'id': 2,
        'titre': 'Règlement des confrontations en direct',
        'type': 'info',
        'contenu': 'Chaque prestation doit être originale, respecter la charte de fair-play scolaire et valoriser l\'expression littéraire en milieu académique.',
        'date': '28 Oct 2026',
        'lu': True,
    },
]

# ---------------------------------------------------------------------------
# 7. PHASES DE LA COMPÉTITION
# ---------------------------------------------------------------------------
PHASES = [
    {'id': 1, 'nom': 'Inscriptions & Dépôts', 'statut': 'termine', 'date': '01 - 15 Octobre 2026'},
    {'id': 2, 'nom': 'Sélection des Candidats', 'statut': 'termine', 'date': '16 - 22 Octobre 2026'},
    {'id': 3, 'nom': 'Quarts de Finale', 'statut': 'termine', 'date': '23 - 31 Octobre 2026'},
    {'id': 4, 'nom': 'Demi-Finales', 'statut': 'en_cours', 'date': '01 - 15 Novembre 2026'},
    {'id': 5, 'nom': 'Grande Finale Abidjan', 'statut': 'a_venir', 'date': '25 Novembre 2026'},
]

# ---------------------------------------------------------------------------
# 8. CHIFFRES CLÉS DE SYNTHÈSE
# ---------------------------------------------------------------------------
STATS_GENERALES = {
    'total_candidats': 6,
    'total_votes': 6630,
    'votes_premium': 1450,
    'total_duels': 3,
    'duels_en_cours': 2,
    'etablissements': 8,
    'categories': 3,
    'montant_transactions': 285000,
}

# ---------------------------------------------------------------------------
# FONCTIONS UTILITAIRES DE RECHERCHE ET D'ENRICHISSEMENT
# Simulent les jointures relationnelles du futur ORM Django
# ---------------------------------------------------------------------------

def get_candidat_by_id(candidat_id):
    """Retourne le candidat correspondant à l'identifiant numérique."""
    for c in CANDIDATS:
        if c['id'] == candidat_id:
            return c
    return None

def get_etablissement_by_id(etab_id):
    """Retourne l'établissement associé à l'identifiant."""
    for e in ETABLISSEMENTS:
        if e['id'] == etab_id:
            return e
    return None

def get_categorie_by_id(cat_id):
    """Retourne la catégorie scolaire ou universitaire."""
    for c in CATEGORIES:
        if c['id'] == cat_id:
            return c
    return None

def enrich_candidat(candidat):
    """
    Enrichit l'objet candidat avec les données complètes de son établissement
    et de sa catégorie, facilitant le travail dans les templates HTML Django.
    """
    if not candidat:
        return None
    c = dict(candidat)
    c['etablissement'] = get_etablissement_by_id(c['etablissement_id'])
    c['categorie'] = get_categorie_by_id(c['categorie_id'])
    return c

def get_all_candidats_enriched():
    """Retourne l'ensemble des candidats avec leurs informations associées."""
    return [enrich_candidat(c) for c in CANDIDATS]

def get_duel_by_id(duel_id):
    """
    Retourne une confrontation enrichie avec les profils complets
    des deux candidats et les pourcentages calculés des votes.
    """
    for d in DUELS:
        if d['id'] == duel_id:
            d_copy = dict(d)
            d_copy['candidat1'] = enrich_candidat(get_candidat_by_id(d['candidat1_id']))
            d_copy['candidat2'] = enrich_candidat(get_candidat_by_id(d['candidat2_id']))
            total = d['votes1'] + d['votes2']
            d_copy['pct1'] = round((d['votes1'] / total) * 100) if total > 0 else 50
            d_copy['pct2'] = round((d['votes2'] / total) * 100) if total > 0 else 50
            return d_copy
    return None

def get_all_duels_enriched():
    """Retourne la liste de tous les duels enrichis."""
    return [get_duel_by_id(d['id']) for d in DUELS]

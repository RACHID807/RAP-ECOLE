"""
Module d'intégration Brevo (ex-Sendinblue) pour RAP CLASH SCHOOL.
Envoi des notifications par courriel lors de la validation des votes.

Courriel d'expédition officiel : rap.ivoire.ecole@gmail.com
API Brevo : https://api.brevo.com/v3/smtp/email
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime

# Configuration officielle
BREVO_API_KEY = os.environ.get('BREVO_API_KEY', '')
SENDER_EMAIL = "rap.ivoire.ecole@gmail.com"
SENDER_NAME = "RAP CLASH SCHOOL Côte d'Ivoire"


def generer_corps_email_html(votant_nom, candidat_nom, nb_voix, montant, telephone, date_heure):
    """Génère un modèle HTML élégant aux couleurs de RAP CLASH SCHOOL."""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="utf-8"/>
  <style>
    body {{
      font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
      background-color: #0A0A12;
      color: #E2E8F0;
      margin: 0;
      padding: 20px;
    }}
    .container {{
      max-width: 600px;
      margin: 0 auto;
      background-color: #121220;
      border: 1px solid #24243D;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}
    .header {{
      background: linear-gradient(135deg, #FF6B00, #9C27B0);
      padding: 30px 20px;
      text-align: center;
      color: #FFFFFF;
    }}
    .logo {{
      font-size: 26px;
      font-weight: 900;
      letter-spacing: 2px;
      text-transform: uppercase;
      margin: 0;
    }}
    .subtitle {{
      font-size: 13px;
      letter-spacing: 1px;
      opacity: 0.9;
      margin-top: 5px;
    }}
    .content {{
      padding: 30px 25px;
      line-height: 1.6;
    }}
    .badge {{
      display: inline-block;
      background-color: rgba(0, 230, 118, 0.15);
      border: 1px solid #00E676;
      color: #00E676;
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: bold;
      text-transform: uppercase;
      margin-bottom: 20px;
    }}
    .card-recap {{
      background-color: #1A1A2E;
      border: 1px solid #333355;
      border-radius: 12px;
      padding: 20px;
      margin: 20px 0;
    }}
    .recap-item {{
      display: flex;
      justify-content: space-between;
      padding: 8px 0;
      border-bottom: 1px solid #252542;
      font-size: 14px;
    }}
    .recap-item:last-child {{
      border-bottom: none;
    }}
    .label {{
      color: #94A3B8;
    }}
    .value {{
      font-weight: bold;
      color: #FFFFFF;
    }}
    .highlight {{
      color: #FFC107;
      font-size: 18px;
    }}
    .footer {{
      background-color: #0B0B14;
      padding: 20px;
      text-align: center;
      font-size: 12px;
      color: #64748B;
      border-top: 1px solid #1E1E34;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1 class="logo">RAP CLASH SCHOOL</h1>
      <div class="subtitle">Championnat Inter-Établissements · Côte d'Ivoire</div>
    </div>
    <div class="content">
      <div class="badge">✓ Vote Validé Officiellement</div>
      <h2 style="color: #FFFFFF; font-size: 20px; margin-top: 0;">Félicitations {votant_nom} !</h2>
      <p style="color: #CBD5E1; font-size: 14px;">
        Votre paiement <strong>Wave ({montant} FCFA)</strong> avec le numéro <strong>{telephone}</strong> a été certifié par l'administration.
      </p>
      <p style="color: #CBD5E1; font-size: 14px;">
        Votre soutien a bien été crédité au compteur de votre artiste en direct dans l'arène.
      </p>

      <div class="card-recap">
        <div class="recap-item">
          <span class="label">Rappeur soutenu</span>
          <span class="value" style="color: #FF6B00;">{candidat_nom}</span>
        </div>
        <div class="recap-item">
          <span class="label">Suffrages crédités</span>
          <span class="value highlight">+{nb_voix} voix</span>
        </div>
        <div class="recap-item">
          <span class="label">Montant du vote</span>
          <span class="value">{montant} FCFA</span>
        </div>
        <div class="recap-item">
          <span class="label">Moyen de paiement</span>
          <span class="value">Wave CI (Validé)</span>
        </div>
        <div class="recap-item">
          <span class="label">Date & Heure</span>
          <span class="value">{date_heure}</span>
        </div>
      </div>

      <p style="font-size: 13px; color: #94A3B8; margin-top: 25px;">
        Continuez à suivre les clashs en direct et les classements sur la plateforme officielle :
        <br/>
        <a href="https://rapclashschool.ci" style="color: #00E5FF; text-decoration: none; font-weight: bold;">Accéder à RAP CLASH SCHOOL →</a>
      </p>
    </div>
    <div class="footer">
      <p style="margin: 0 0 5px 0;">Comité d'Organisation RAP CLASH SCHOOL (RCS)</p>
      <p style="margin: 0;">Courriel : {SENDER_EMAIL} · Abidjan, Côte d'Ivoire</p>
    </div>
  </div>
</body>
</html>"""


def envoyer_confirmation_vote_brevo(votant_nom, votant_email, candidat_nom, nb_voix=1, montant=500, telephone=""):
    """
    Envoie un courriel transactionnel via l'API Brevo.
    Si BREVO_API_KEY est absente, simule proprement l'envoi pour le développement local.
    """
    if not votant_email:
        return False, "Aucune adresse courriel fournie."

    maintenant = datetime.now().strftime("%d/%m/%Y à %H:%M")
    html_content = generer_corps_email_html(
        votant_nom=votant_nom,
        candidat_nom=candidat_nom,
        nb_voix=nb_voix,
        montant=montant,
        telephone=telephone,
        date_heure=maintenant,
    )

    api_key = os.environ.get('BREVO_API_KEY', '').strip()

    if not api_key:
        # Mode développement / simulation sécurisée
        print(f"[BREVO SIMULATION] Email envoyé à {votant_email} pour le vote de {candidat_nom} (+{nb_voix} voix). Expéditeur: {SENDER_EMAIL}")
        return True, "Simulation : Courriel de validation généré avec succès (ajoutez BREVO_API_KEY pour l'envoi réel en production)."

    # Envoi réel via l'API REST v3 de Brevo
    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": SENDER_NAME,
            "email": SENDER_EMAIL
        },
        "to": [
            {
                "email": votant_email,
                "name": votant_nom or "Votant RAP CLASH SCHOOL"
            }
        ],
        "subject": f"✓ Confirmation de votre vote pour {candidat_nom} — RAP CLASH SCHOOL",
        "htmlContent": html_content
    }

    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status in [200, 201, 202]:
                return True, f"Courriel Brevo envoyé avec succès à {votant_email}."
            return False, f"Code réponse Brevo inattendu : {response.status}"
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode('utf-8', errors='ignore')
        print(f"[BREVO ERREUR HTTP] {e.code}: {error_msg}")
        return False, f"Erreur Brevo ({e.code}) : {error_msg}"
    except Exception as e:
        print(f"[BREVO ERREUR EXCEPTION] {e}")
        return False, f"Erreur de connexion Brevo : {e}"

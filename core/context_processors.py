"""
Processeurs de contexte pour rendre disponibles les informations globales
(Message défilant du bandeau, lien WhatsApp, lien Wave) sur l'ensemble des pages.
"""

from .data import MESSAGE_DEFILANT, WHATSAPP_URL, WAVE_PAY_URL

def site_global_context(request):
    """Injecte les variables globales de RAP CLASH SCHOOL dans tous les gabarits."""
    return {
        'message_defilant': MESSAGE_DEFILANT,
        'whatsapp_url': WHATSAPP_URL,
        'wave_pay_url': WAVE_PAY_URL,
    }

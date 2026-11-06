from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('candidats/', views.candidats_list, name='candidats'),
    path('candidats/<int:pk>/', views.candidat_detail, name='candidat_detail'),
    path('duels/', views.duels_list, name='duels'),
    path('duels/<int:pk>/', views.duel_detail, name='duel_detail'),
    path('vote/<int:candidat_id>/', views.vote_page, name='vote'),
    path('classement/', views.classement, name='classement'),

    # Espace candidat
    path('espace-candidat/', views.espace_candidat, name='espace_candidat'),
    path('espace-candidat/profil/', views.candidat_profil, name='candidat_profil'),
    path('espace-candidat/medias/', views.candidat_medias, name='candidat_medias'),
    path('espace-candidat/duels/', views.candidat_duels_view, name='candidat_duels'),
    path('espace-candidat/notifications/', views.candidat_notifications, name='candidat_notifications'),

    # Admin panel
    path('admin-panel/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-panel/candidats/', views.admin_candidats, name='admin_candidats'),
    path('admin-panel/votes/', views.admin_votes, name='admin_votes'),
    path('admin-panel/duels/', views.admin_duels, name='admin_duels'),
    path('admin-panel/transactions/', views.admin_transactions, name='admin_transactions'),
    path('admin-panel/annonces/', views.admin_annonces, name='admin_annonces'),
    path('admin-panel/parametres/', views.admin_parametres, name='admin_parametres'),

    # Auth
    path('inscription/', views.inscription, name='inscription'),
    path('connexion/', views.connexion, name='connexion'),
]

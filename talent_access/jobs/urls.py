from django.urls import path
from . import views

urlpatterns = [
    path('offres/', views.liste_offres, name='liste_offres'),
    path('offres/<int:offre_id>/', views.offre_detail, name='offre_detail'),
    path('offres/<int:offre_id>/postuler/', views.postuler_offre, name='postuler_offre'),
    path('offres/nouvelle/', views.creer_offre, name='creer_offre'),
    path('mes-offres/<int:offre_id>/', views.offre_pme_detail, name='voir_offre_pme'),
    path('mes-offres/<int:offre_id>/modifier/', views.modifier_offre, name='modifier_offre'),
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('candidatures-recues/', views.candidatures_recues, name='candidatures_recues'),
    path('candidatures/<int:candidature_id>/', views.candidature_detail, name='candidature_detail'),
]

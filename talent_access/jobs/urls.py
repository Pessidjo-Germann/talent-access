from django.urls import path
from . import views

urlpatterns = [
    path('offres/<int:offre_id>/', views.offre_detail, name='offre_detail'),
    path('offres/<int:offre_id>/postuler/', views.postuler_offre, name='postuler_offre'),
    path('offres/nouvelle/', views.creer_offre, name='creer_offre'),
    path('mes-candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('candidatures-recues/', views.candidatures_recues, name='candidatures_recues'),
]

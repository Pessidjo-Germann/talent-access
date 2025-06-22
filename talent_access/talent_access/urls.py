from django.contrib import admin
from django.urls import path, include
from users import views as user_views
from profiles import views as profile_views
from django.contrib.auth import views as auth_views  # Ajouté pour logout

urlpatterns = [
    path('', user_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('diplome/signup/', user_views.diplome_signup, name='diplome_signup'),
    path('pme/signup/', user_views.pme_signup, name='pme_signup'),
    path('diplome/login/', user_views.diplome_login, name='diplome_login'),
    path('pme/login/', user_views.pme_login, name='pme_login'),
    path('diplome/dashboard/', user_views.diplome_dashboard, name='diplome_dashboard'),
    path('pme/dashboard/', user_views.pme_dashboard, name='pme_dashboard'),
 
    path('diplome/profil/', profile_views.voir_profil_diplome, name='voir_profil_diplome'),
    path('diplome/profil/modifier/', profile_views.modifier_profil_diplome, name='modifier_profil_diplome'),

    path('pme/profil/', profile_views.voir_profil_pme, name='voir_profil_pme'),
    path('pme/profil/modifier/', profile_views.modifier_profil_pme, name='modifier_profil_pme'),

    path('logout/', auth_views.LogoutView.as_view(next_page='diplome_login'), name='logout'),
    path('jobs/', include('jobs.urls')),
    path('messages/', include('messagerie.urls')),
 
]

from django.contrib import admin
from django.urls import path
from users import views as user_views

urlpatterns = [
    path('', user_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('diplome/signup/', user_views.diplome_signup, name='diplome_signup'),
    path('pme/signup/', user_views.pme_signup, name='pme_signup'),
    path('diplome/login/', user_views.diplome_login, name='diplome_login'),
    path('pme/login/', user_views.pme_login, name='pme_login'),
    path('diplome/dashboard/', user_views.diplome_dashboard, name='diplome_dashboard'),
    path('pme/dashboard/', user_views.pme_dashboard, name='pme_dashboard'),
]

from django.urls import path
from . import views

app_name = 'activites'

urlpatterns = [
    path('', views.liste_activites, name='liste_activites'),
    path('creer/', views.creer_sport, name='creer_activite'),
    path('<int:sport_id>/', views.detail_activite, name='detail_activite'),
    path('<int:sport_id>/modifier/', views.modifier_sport, name='modifier_activite'),
    path('<int:sport_id>/supprimer/', views.supprimer_sport, name='supprimer_activite'),
] 
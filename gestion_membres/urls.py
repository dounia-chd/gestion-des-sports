from django.urls import path
from . import views

app_name = 'membres'

urlpatterns = [
    path('', views.liste_membres, name='liste_membres'),
    path('creer/', views.creer_membre, name='creer_membre'),
    path('<int:membre_id>/', views.detail_membre, name='detail_membre'),
    path('<int:membre_id>/modifier/', views.modifier_membre, name='modifier_membre'),
    path('<int:membre_id>/supprimer/', views.supprimer_membre, name='supprimer_membre'),
] 
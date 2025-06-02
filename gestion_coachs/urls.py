from django.urls import path
from . import views

app_name = 'coachs'

urlpatterns = [
    path('', views.liste_coachs, name='liste_coachs'),
    path('supprimer/<int:coach_id>/', views.supprimer_coach, name='supprimer_coach'),
] 
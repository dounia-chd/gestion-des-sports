from django.urls import path
from . import views

app_name = 'salles'

urlpatterns = [
    path('', views.liste_salles, name='liste_salles'),
] 
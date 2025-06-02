from django.contrib import admin
from .models import Niveau, Sport, Horaire

@admin.register(Niveau)
class NiveauAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('nom', 'niveau_requis', 'capacite_max', 'duree_seance', 'prix', 'actif')
    list_filter = ('niveau_requis', 'actif')
    search_fields = ('nom', 'description')

@admin.register(Horaire)
class HoraireAdmin(admin.ModelAdmin):
    list_display = ('sport', 'jour', 'heure_debut', 'heure_fin', 'salle')
    list_filter = ('jour', 'sport', 'salle')
    search_fields = ('sport__nom', 'salle__nom')

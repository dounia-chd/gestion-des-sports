from django.contrib import admin
from .models import Salle, Equipement

@admin.register(Salle)
class SalleAdmin(admin.ModelAdmin):
    list_display = ('nom', 'capacite', 'superficie', 'disponible')
    list_filter = ('disponible',)
    search_fields = ('nom', 'description')

@admin.register(Equipement)
class EquipementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'quantite', 'salle')
    list_filter = ('salle',)
    search_fields = ('nom', 'description')

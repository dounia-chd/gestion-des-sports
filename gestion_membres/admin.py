from django.contrib import admin
from .models import Membre, Inscription

@admin.register(Membre)
class MembreAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_naissance', 'telephone', 'date_inscription')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'telephone')
    list_filter = ('date_inscription',)
    readonly_fields = ('date_inscription',)

@admin.register(Inscription)
class InscriptionAdmin(admin.ModelAdmin):
    list_display = ('membre', 'sport', 'date_inscription', 'date_fin', 'active')
    list_filter = ('active', 'date_inscription', 'date_fin')
    search_fields = ('membre__user__username', 'sport__nom')
    readonly_fields = ('date_inscription',)

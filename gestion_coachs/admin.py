from django.contrib import admin
from .models import Coach

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience', 'telephone', 'email', 'disponible')
    list_filter = ('disponible', 'specialites')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'email', 'telephone')
    filter_horizontal = ('specialites',)

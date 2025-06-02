from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import date, timedelta

# Import your models
from gestion_membres.models import Membre
from gestion_coachs.models import Coach
from gestion_activites.models import Sport, Seance, InscriptionSport
from gestion_reservations.models import Reservation

@staff_member_required
def admin_dashboard(request):
    # Get counts for the dashboard
    today = date.today()
    start_of_month = today.replace(day=1)
    
    context = {
        'total_membres': Membre.objects.count(),
        'activites_actives': Sport.objects.filter(actif=True).count(),
        'seances_aujourdhui': Seance.objects.filter(date=today).count(),
        'revenus_mois': InscriptionSport.objects.filter(
            date_inscription__month=today.month,
            date_inscription__year=today.year
        ).aggregate(total=Sum('sport__prix'))['total'] or 0,
        'sports': Sport.objects.all().order_by('-id')[:5],  # Using id for ordering since date_creation doesn't exist
        'seances_a_venir': Seance.objects.filter(date__gte=today).order_by('date', 'heure_debut')[:5],
        'dernieres_inscriptions': InscriptionSport.objects.select_related('membre', 'sport').order_by('-date_inscription')[:5]
    }
    return render(request, 'admin/dashboard.html', context)

# Custom admin site
class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(admin_dashboard), name='admin_dashboard'),
        ]
        return custom_urls + urls

# Create an instance of the custom admin site
admin_site = CustomAdminSite(name='custom_admin')

# Register your models with the custom admin site
from django.contrib.auth.models import Group, User
admin_site.register(Group)
admin_site.register(User)
admin_site.register(Membre)
admin_site.register(Coach)
admin_site.register(Sport)
admin_site.register(Seance)
admin_site.register(Reservation)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from .models import Sport, Niveau, Horaire, Seance
from .forms import SportForm

# Create your views here.

def liste_activites(request):
    # Récupérer les paramètres de filtrage
    niveau_id = request.GET.get('niveau')
    status = request.GET.get('status')
    search = request.GET.get('search')
    
    # Récupérer tous les niveaux pour le filtre
    niveaux = Niveau.objects.all()
    
    # Filtrer les sports
    sports = Sport.objects.select_related('niveau_requis').all()
    
    if niveau_id:
        sports = sports.filter(niveau_requis_id=niveau_id)
    if status:
        sports = sports.filter(actif=(status == 'actif'))
    if search:
        sports = sports.filter(
            Q(nom__icontains=search) | 
            Q(description__icontains=search)
        )
    
    # Calculer les statistiques
    total_seances = Seance.objects.count()
    
    context = {
        'sports': sports,
        'niveaux': niveaux,
        'total_seances': total_seances,
        'selected_niveau': niveau_id,
        'selected_status': status,
        'search_query': search
    }
    return render(request, 'gestion_activites/liste_activites.html', context)

@login_required
@transaction.atomic
def creer_sport(request):
    if request.method == 'POST':
        form = SportForm(request.POST, request.FILES)
        if form.is_valid():
            sport = form.save()
            messages.success(request, 'L\'activité a été créée avec succès.')
            return redirect('activites:detail_activite', sport_id=sport.id)
    else:
        form = SportForm()
    
    return render(request, 'gestion_activites/form_sport.html', {'form': form})

@login_required
@transaction.atomic
def modifier_sport(request, sport_id):
    sport = get_object_or_404(Sport, id=sport_id)
    if request.method == 'POST':
        form = SportForm(request.POST, request.FILES, instance=sport)
        if form.is_valid():
            form.save()
            messages.success(request, 'L\'activité a été modifiée avec succès.')
            return redirect('activites:detail_activite', sport_id=sport.id)
    else:
        form = SportForm(instance=sport)
    
    return render(request, 'gestion_activites/form_sport.html', {'form': form})

@login_required
@transaction.atomic
def supprimer_sport(request, sport_id):
    sport = get_object_or_404(Sport, id=sport_id)
    if request.method == 'POST':
        sport.delete()
        messages.success(request, 'L\'activité a été supprimée avec succès.')
        return redirect('activites:liste_activites')
    
    return render(request, 'gestion_activites/confirmer_suppression.html', {'sport': sport})

def detail_activite(request, sport_id):
    sport = get_object_or_404(Sport.objects.select_related('niveau_requis'), id=sport_id)
    seances = sport.seances.all().order_by('date', 'heure_debut')
    return render(request, 'gestion_activites/detail_activite.html', {
        'sport': sport,
        'seances': seances
    })

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.db import transaction
from .models import Membre
from .forms import MembreForm  # À créer

# Create your views here.

@login_required
def liste_membres(request):
    try:
        # Recherche
        query = request.GET.get('q')
        if query:
            membres = Membre.objects.filter(
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query) |
                Q(telephone__icontains=query)
            ).select_related('user')
        else:
            membres = Membre.objects.all().select_related('user')
        
        # Pagination
        paginator = Paginator(membres, 10)  # 10 membres par page
        page = request.GET.get('page')
        membres = paginator.get_page(page)
        
        return render(request, 'gestion_membres/liste_membres.html', {
            'membres': membres,
            'query': query
        })
    except Exception as e:
        messages.error(request, f"Une erreur est survenue lors du chargement de la liste des membres: {str(e)}")
        return redirect('home')

@login_required
def detail_membre(request, membre_id):
    try:
        membre = get_object_or_404(Membre, id=membre_id)
        inscriptions = membre.inscriptions.all().select_related('sport')
        return render(request, 'gestion_membres/detail_membre.html', {
            'membre': membre,
            'inscriptions': inscriptions
        })
    except Exception as e:
        messages.error(request, f"Une erreur est survenue lors du chargement des détails du membre: {str(e)}")
        return redirect('membres:liste_membres')

@login_required
@transaction.atomic
def creer_membre(request):
    try:
        if request.method == 'POST':
            form = MembreForm(request.POST)
            if form.is_valid():
                membre = form.save()
                messages.success(request, "Le membre a été créé avec succès.")
                return redirect('membres:detail_membre', membre_id=membre.id)
            else:
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        else:
            form = MembreForm()
        return render(request, 'gestion_membres/form_membre.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Une erreur est survenue lors de la création du membre: {str(e)}")
        return redirect('membres:liste_membres')

@login_required
@transaction.atomic
def modifier_membre(request, membre_id):
    try:
        membre = get_object_or_404(Membre, id=membre_id)
        if request.method == 'POST':
            form = MembreForm(request.POST, instance=membre)
            if form.is_valid():
                form.save()
                messages.success(request, "Les modifications ont été enregistrées avec succès.")
                return redirect('membres:detail_membre', membre_id=membre.id)
            else:
                messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
        else:
            form = MembreForm(instance=membre)
        return render(request, 'gestion_membres/form_membre.html', {'form': form})
    except Exception as e:
        messages.error(request, f"Une erreur est survenue lors de la modification du membre: {str(e)}")
        return redirect('membres:liste_membres')

@login_required
@transaction.atomic
def supprimer_membre(request, membre_id):
    try:
        membre = get_object_or_404(Membre, id=membre_id)
        if request.method == 'POST':
            try:
                user = membre.user
                membre.delete()
                user.delete()
                messages.success(request, "Le membre a été supprimé avec succès.")
            except Exception as e:
                messages.error(request, f"Erreur lors de la suppression du membre: {str(e)}")
            return redirect('membres:liste_membres')
        return render(request, 'gestion_membres/confirmer_suppression.html', {'membre': membre})
    except Exception as e:
        messages.error(request, f"Une erreur est survenue lors de la suppression du membre: {str(e)}")
        return redirect('membres:liste_membres')

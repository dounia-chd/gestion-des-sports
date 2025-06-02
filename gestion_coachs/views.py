from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Coach

# Create your views here.

def liste_coachs(request):
    coachs = Coach.objects.all().select_related('user').prefetch_related('sports')
    return render(request, 'gestion_coachs/liste_coachs.html', {'coachs': coachs})

def supprimer_coach(request, coach_id):
    coach = get_object_or_404(Coach, id=coach_id)
    try:
        user = coach.user
        coach.delete()
        user.delete()
        messages.success(request, "Le coach a été supprimé avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors de la suppression du coach: {str(e)}")
    return redirect('coachs:liste_coachs')

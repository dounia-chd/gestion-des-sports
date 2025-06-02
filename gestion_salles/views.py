from django.shortcuts import render
from .models import Salle

# Create your views here.

def liste_salles(request):
    salles = Salle.objects.all().prefetch_related('equipements')
    return render(request, 'gestion_salles/liste_salles.html', {'salles': salles})

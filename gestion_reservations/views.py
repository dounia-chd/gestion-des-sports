from django.shortcuts import render
from .models import Reservation

# Create your views here.

def liste_reservations(request):
    reservations = Reservation.objects.all().select_related('membre', 'seance', 'seance__sport')
    return render(request, 'gestion_reservations/liste_reservations.html', {'reservations': reservations})

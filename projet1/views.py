from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from gestion_membres.models import Membre
from gestion_coachs.models import Coach
from gestion_activites.models import Sport, Niveau, Horaire, InscriptionSport, Seance
from gestion_salles.models import Salle
from django.db.models import Count, Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('client_dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'registration/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('client_dashboard')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return render(request, 'registration/login.html')
    
    return render(request, 'registration/login.html')

def client_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('client_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'registration/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                messages.error(request, "Veuillez utiliser l'espace administrateur.")
                return redirect('admin_login')
            
            # Vérifier si l'utilisateur a un profil membre
            try:
                Membre.objects.get(user=user)
                login(request, user)
                messages.success(request, f"Bienvenue {user.username} !")
                return redirect('client_dashboard')
            except Membre.DoesNotExist:
                messages.error(request, "Votre compte n'est pas correctement configuré. Veuillez contacter l'administrateur.")
                return render(request, 'registration/login.html')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return render(request, 'registration/login.html')
    
    return render(request, 'registration/login.html')

def admin_login(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            return redirect('client_dashboard')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'registration/login.html')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if not user.is_staff:
                messages.error(request, "Vous n'avez pas les droits d'administrateur.")
                return redirect('client_login')
            
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return render(request, 'registration/login.html')
    
    return render(request, 'registration/login.html')

def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('client_dashboard')
    return render(request, 'home.html')

@login_required
def client_dashboard(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')
    
    try:
        membre = Membre.objects.get(user=request.user)
        inscriptions = membre.inscriptions.all().select_related('sport')
        
        # Récupérer les séances à venir pour les activités auxquelles le membre est inscrit
        seances = []
        for inscription in inscriptions.filter(active=True):
            seances.extend(inscription.sport.seances.filter(date__gte=timezone.now().date()))
        
        # Trier les séances par date
        seances.sort(key=lambda x: (x.date, x.heure_debut))
        
        return render(request, 'client/dashboard.html', {
            'membre': membre,
            'inscriptions': inscriptions,
            'seances': seances,
            'now': timezone.now()
        })
    except Membre.DoesNotExist:
        messages.error(request, "Votre profil n'est pas correctement configuré.")
        return redirect('logout')

@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('client_dashboard')
    
    # Statistiques pour le tableau de bord
    total_membres = Membre.objects.count()
    activites_actives = Sport.objects.filter(actif=True).count()
    seances_aujourdhui = Seance.objects.filter(date=timezone.now().date()).count()
    
    # Calculer les revenus du mois
    debut_mois = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    revenus_mois = InscriptionSport.objects.filter(
        date_inscription__gte=debut_mois
    ).aggregate(total=Sum('sport__prix'))['total'] or 0
    
    # Récupérer les activités récentes
    sports = Sport.objects.all().order_by('-id')[:10]
    
    # Récupérer les séances à venir
    seances = Seance.objects.filter(
        date__gte=timezone.now().date()
    ).select_related('sport', 'instructeur', 'salle').order_by('date', 'heure_debut')[:5]
    
    return render(request, 'admin/dashboard.html', {
        'total_membres': total_membres,
        'activites_actives': activites_actives,
        'seances_aujourdhui': seances_aujourdhui,
        'revenus_mois': revenus_mois,
        'sports': sports,
        'seances': seances
    })

def logout_view(request):
    logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('home')

class MembreRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    telephone = forms.CharField(max_length=15, required=True)
    adresse = forms.CharField(max_length=200, required=True)
    date_naissance = forms.DateField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Créer le profil membre associé
            Membre.objects.create(
                user=user,
                telephone=self.cleaned_data['telephone'],
                adresse=self.cleaned_data['adresse'],
                date_naissance=self.cleaned_data['date_naissance']
            )
        return user

def register(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = MembreRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Votre compte a été créé avec succès !")
            return redirect('client_dashboard')
    else:
        form = MembreRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form}) 
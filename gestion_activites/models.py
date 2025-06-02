from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from gestion_membres.models import Membre
from django.utils import timezone

# Create your models here.

class Niveau(models.Model):
    nom = models.CharField(max_length=50, verbose_name=_("Nom"))
    description = models.TextField(verbose_name=_("Description"))
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = _("Niveau")
        verbose_name_plural = _("Niveaux")

class Sport(models.Model):
    nom = models.CharField(max_length=100, verbose_name=_("Nom"))
    description = models.TextField(verbose_name=_("Description"))
    niveau_requis = models.ForeignKey(
        Niveau, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='sports',
        verbose_name=_("Niveau requis")
    )
    capacite_max = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name=_("Capacité maximale")
    )
    duree_seance = models.PositiveIntegerField(
        help_text=_("Durée en minutes"),
        validators=[MinValueValidator(15), MaxValueValidator(180)],
        verbose_name=_("Durée de la séance")
    )
    prix = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name=_("Prix")
    )
    image = models.ImageField(
        upload_to='sports/',
        null=True,
        blank=True,
        verbose_name=_("Image")
    )
    actif = models.BooleanField(
        default=True,
        verbose_name=_("Actif")
    )
    
    def clean(self):
        if self.niveau_requis is None:
            raise ValidationError(_("Le niveau requis est obligatoire."))
        
        if self.capacite_max < 1:
            raise ValidationError(_("La capacité maximale doit être supérieure à 0."))
        
        if self.duree_seance < 15 or self.duree_seance > 180:
            raise ValidationError(_("La durée de la séance doit être comprise entre 15 et 180 minutes."))
        
        if self.prix < 0:
            raise ValidationError(_("Le prix ne peut pas être négatif."))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = _("Sport")
        verbose_name_plural = _("Sports")

class Horaire(models.Model):
    JOURS_SEMAINE = [
        ('LUN', _('Lundi')),
        ('MAR', _('Mardi')),
        ('MER', _('Mercredi')),
        ('JEU', _('Jeudi')),
        ('VEN', _('Vendredi')),
        ('SAM', _('Samedi')),
        ('DIM', _('Dimanche')),
    ]
    
    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        related_name='horaires',
        verbose_name=_("Sport")
    )
    jour = models.CharField(
        max_length=3,
        choices=JOURS_SEMAINE,
        verbose_name=_("Jour")
    )
    heure_debut = models.TimeField(verbose_name=_("Heure de début"))
    heure_fin = models.TimeField(verbose_name=_("Heure de fin"))
    salle = models.ForeignKey(
        'gestion_salles.Salle',
        on_delete=models.CASCADE,
        related_name='horaires',
        verbose_name=_("Salle")
    )
    
    def clean(self):
        if self.heure_fin <= self.heure_debut:
            raise ValidationError(_("L'heure de fin doit être postérieure à l'heure de début."))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.sport.nom} - {self.get_jour_display()} {self.heure_debut}-{self.heure_fin}"
    
    class Meta:
        verbose_name = _("Horaire")
        verbose_name_plural = _("Horaires")
        unique_together = ['sport', 'jour', 'heure_debut', 'salle']

class InscriptionSport(models.Model):
    membre = models.ForeignKey(
        Membre,
        on_delete=models.CASCADE,
        related_name='inscriptions_sport',
        verbose_name=_("Membre")
    )
    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        related_name='inscriptions_sport',
        verbose_name=_("Sport")
    )
    date_debut = models.DateField(verbose_name=_("Date de début"))
    date_fin = models.DateField(verbose_name=_("Date de fin"))
    date_inscription = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date d'inscription")
    )
    
    def clean(self):
        if self.date_fin < self.date_debut:
            raise ValidationError(_("La date de fin doit être postérieure à la date de début."))
        
        # Vérifier si le membre est déjà inscrit à ce sport
        if InscriptionSport.objects.filter(
            membre=self.membre,
            sport=self.sport,
            date_fin__gte=self.date_debut,
            date_debut__lte=self.date_fin
        ).exclude(id=self.id).exists():
            raise ValidationError(_("Vous êtes déjà inscrit à ce sport pour cette période."))
        
        # Vérifier si le sport a atteint sa capacité maximale
        nombre_inscriptions = InscriptionSport.objects.filter(
            sport=self.sport,
            date_fin__gte=self.date_debut,
            date_debut__lte=self.date_fin
        ).exclude(id=self.id).count()
        
        if nombre_inscriptions >= self.sport.capacite_max:
            raise ValidationError(_("Ce sport a atteint sa capacité maximale pour cette période."))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.membre.user.username} - {self.sport.nom} ({self.date_debut} au {self.date_fin})"
    
    class Meta:
        verbose_name = _("Inscription à un sport")
        verbose_name_plural = _("Inscriptions aux sports")
        unique_together = ['membre', 'sport', 'date_debut', 'date_fin']

class Seance(models.Model):
    sport = models.ForeignKey(
        Sport,
        on_delete=models.CASCADE,
        related_name='seances',
        verbose_name=_("Sport")
    )
    date = models.DateField(verbose_name=_("Date"))
    heure_debut = models.TimeField(verbose_name=_("Heure de début"))
    heure_fin = models.TimeField(verbose_name=_("Heure de fin"))
    instructeur = models.ForeignKey(
        'gestion_coachs.Coach',
        on_delete=models.SET_NULL,
        null=True,
        related_name='seances',
        verbose_name=_("Instructeur")
    )
    salle = models.ForeignKey(
        'gestion_salles.Salle',
        on_delete=models.CASCADE,
        related_name='seances',
        verbose_name=_("Salle")
    )
    places_disponibles = models.PositiveIntegerField(
        default=0,
        verbose_name=_("Places disponibles")
    )
    
    def clean(self):
        if self.heure_fin <= self.heure_debut:
            raise ValidationError(_("L'heure de fin doit être postérieure à l'heure de début."))
        
        if self.date < timezone.now().date():
            raise ValidationError(_("La date ne peut pas être dans le passé."))
        
        if self.places_disponibles > self.sport.capacite_max:
            raise ValidationError(_("Le nombre de places disponibles ne peut pas dépasser la capacité maximale du sport."))
    
    def save(self, *args, **kwargs):
        if not self.places_disponibles:
            self.places_disponibles = self.sport.capacite_max
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.sport.nom} - {self.date} {self.heure_debut}-{self.heure_fin}"
    
    class Meta:
        verbose_name = _("Séance")
        verbose_name_plural = _("Séances")
        ordering = ['date', 'heure_debut']
        unique_together = ['sport', 'date', 'heure_debut', 'salle']

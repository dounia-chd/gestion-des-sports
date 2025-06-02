from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

# Create your models here.

class Salle(models.Model):
    nom = models.CharField(
        max_length=100,
        verbose_name=_("Nom")
    )
    capacite = models.PositiveIntegerField(
        help_text=_("Nombre maximum de personnes"),
        validators=[MinValueValidator(1)],
        verbose_name=_("Capacité")
    )
    description = models.TextField(verbose_name=_("Description"))
    superficie = models.PositiveIntegerField(
        help_text=_("Superficie en m²"),
        validators=[MinValueValidator(1)],
        verbose_name=_("Superficie")
    )
    disponible = models.BooleanField(
        default=True,
        verbose_name=_("Disponible")
    )
    
    def __str__(self):
        return self.nom
    
    class Meta:
        verbose_name = _("Salle")
        verbose_name_plural = _("Salles")

class Equipement(models.Model):
    nom = models.CharField(
        max_length=100,
        verbose_name=_("Nom")
    )
    description = models.TextField(verbose_name=_("Description"))
    quantite = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)],
        verbose_name=_("Quantité")
    )
    salle = models.ForeignKey(
        Salle,
        on_delete=models.CASCADE,
        related_name='equipements',
        verbose_name=_("Salle")
    )
    
    def __str__(self):
        return f"{self.nom} ({self.quantite})"
    
    class Meta:
        verbose_name = _("Équipement")
        verbose_name_plural = _("Équipements")

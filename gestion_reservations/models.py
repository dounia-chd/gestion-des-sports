from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from gestion_membres.models import Membre
from gestion_activites.models import Seance

class Reservation(models.Model):
    """
    Model representing a reservation made by a member for a specific session.
    """
    class StatutReservation(models.TextChoices):
        CONFIRMEE = 'CONFIRMEE', _('Confirmée')
        ANNULEE = 'ANNULEE', _('Annulée')
        TERMINEE = 'TERMINEE', _('Terminée')
        EN_ATTENTE = 'EN_ATTENTE', _('En attente')
    
    membre = models.ForeignKey(
        Membre,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name=_('Membre')
    )
    
    seance = models.ForeignKey(
        Seance,
        on_delete=models.CASCADE,
        related_name='reservations',
        verbose_name=_('Séance')
    )
    
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Date de création')
    )
    
    statut = models.CharField(
        max_length=20,
        choices=StatutReservation.choices,
        default=StatutReservation.CONFIRMEE,
        verbose_name=_('Statut')
    )
    
    present = models.BooleanField(
        default=False,
        verbose_name=_('Présent')
    )
    
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Notes')
    )
    
    class Meta:
        verbose_name = _('Réservation')
        verbose_name_plural = _('Réservations')
        ordering = ['-date_creation']
        unique_together = ['membre', 'seance']
    
    def clean(self):
        # Vérifier que la capacité de la séance n'est pas dépassée
        if self.seance.places_disponibles <= 0 and not self.pk:
            raise ValidationError(_("Aucune place disponible pour cette séance."))
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.membre} - {self.seance} ({self.get_statut_display()})"

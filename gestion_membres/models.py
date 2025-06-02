from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.utils import timezone

class Membre(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_naissance = models.DateField()
    telephone = models.CharField(max_length=15)
    adresse = models.TextField()
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()}"

class Inscription(models.Model):
    membre = models.ForeignKey(
        Membre,
        on_delete=models.CASCADE,
        related_name='inscriptions',
        verbose_name=_("Membre")
    )
    sport = models.ForeignKey(
        'gestion_activites.Sport',
        on_delete=models.CASCADE,
        related_name='inscriptions',
        verbose_name=_("Sport")
    )
    date_inscription = models.DateField(
        auto_now_add=True,
        verbose_name=_("Date d'inscription")
    )
    date_fin = models.DateField(verbose_name=_("Date de fin"))
    active = models.BooleanField(
        default=True,
        verbose_name=_("Active")
    )
    
    def clean(self):
        if self.date_fin and self.date_fin < timezone.now().date():
            raise ValidationError(_("La date de fin ne peut pas être dans le passé"))
    
    def __str__(self):
        return f"{self.membre} - {self.sport}"
    
    class Meta:
        verbose_name = _("Inscription")
        verbose_name_plural = _("Inscriptions")
        unique_together = ['membre', 'sport']

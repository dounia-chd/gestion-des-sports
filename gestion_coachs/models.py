from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator

class Coach(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name=_("Utilisateur")
    )
    specialites = models.ManyToManyField(
        'gestion_activites.Sport',
        related_name='coachs',
        verbose_name=_("Spécialités")
    )
    experience = models.PositiveIntegerField(
        help_text=_("Années d'expérience"),
        validators=[MinValueValidator(0)],
        verbose_name=_("Expérience")
    )
    bio = models.TextField(verbose_name=_("Biographie"))
    photo = models.ImageField(
        upload_to='coachs/',
        null=True,
        blank=True,
        verbose_name=_("Photo")
    )
    telephone = models.CharField(
        max_length=15,
        verbose_name=_("Téléphone")
    )
    email = models.EmailField(verbose_name=_("Email"))
    disponible = models.BooleanField(
        default=True,
        verbose_name=_("Disponible")
    )
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
    
    class Meta:
        verbose_name = _("Coach")
        verbose_name_plural = _("Coachs")

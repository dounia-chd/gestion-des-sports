from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GestionMembresConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_membres'
    verbose_name = _("Gestion des Membres")

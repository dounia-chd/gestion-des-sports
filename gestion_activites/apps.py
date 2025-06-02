from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GestionActivitesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gestion_activites'
    verbose_name = _("Gestion des Activités")

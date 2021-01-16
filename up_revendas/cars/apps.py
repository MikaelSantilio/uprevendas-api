from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CarsConfig(AppConfig):
    name = "up_revendas.cars"
    verbose_name = _("Cars")

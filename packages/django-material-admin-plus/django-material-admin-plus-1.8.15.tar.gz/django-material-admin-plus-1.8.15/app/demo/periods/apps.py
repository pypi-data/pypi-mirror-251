from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PeriodsConfig(AppConfig):
    name = 'demo.periods'
    icon_name = 'hourglass_empty'
    verbose_name = _('Periods')

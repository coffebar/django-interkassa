from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _

__version__ = '1.0.0'

default_app_config = 'interkassa_merchant.Config'


class Config(AppConfig):
    name = 'interkassa_merchant'
    verbose_name = _("Interkassa Merchant")
    label = 'interkassa_merchant'

# flake8: noqa
from django.conf import settings

from .defaults import MileaAdmin
from .users import NewUserAdmin

if hasattr(settings, 'USE_MILEA_CHOICES') and settings.USE_MILEA_CHOICES:
    from .choices import MileaChoicesAdmin

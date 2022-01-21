"""Custom types used for type annotations."""

__all__ = ['CurrencyEnum']

from django.db import models
from django.utils.translation import gettext_lazy as _


class CurrencyEnum(models.TextChoices):
    """Allowed funds currencies."""
    USD = 'USD', _('United States dollar')

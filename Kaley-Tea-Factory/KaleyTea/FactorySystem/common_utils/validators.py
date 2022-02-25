from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def nic_validator(value):
    if len(value) < 10:
        raise ValidationError(
            _('%(value)s should have 10 or 12 characters.'),
            params={'value': value},
        )

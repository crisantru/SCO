from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_len(value):
    print("entra validator")
    if not "test" in value:
        raise ValidationError(
            _('%(value)s is not an even number'),
            params={'value': value},
        )

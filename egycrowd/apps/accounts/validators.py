import re
from django.core.exceptions import ValidationError


def validate_egyptian_phone(value):
    
    pattern = re.compile(r'^(?:\+20|0)?1[0125][0-9]{8}$')
    normalized = value.strip().replace(" ", "").replace("-", "")

    if not pattern.match(normalized):
        raise ValidationError(
           "Please enter a valid Egyptian mobile number, for example: 01012345678."
       )
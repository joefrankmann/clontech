import os
import re
from django.core.exceptions import ValidationError


def validate_language_code(value):
    if not re.match(r'^([a-z]{2})(|-[a-z]{2})$', value.lower()):
        raise ValidationError('Language codes must be in ISO format, i.e. en, de, pt-BR (case insensitive).')


def validate_eula_file_size(value):
    """
    Set valid file size here, and in JS if applicable

    2.5MB - 2621440
    5MB - 5242880
    10MB - 10485760
    20MB - 20971520
    50MB - 5242880

    """
    limit = 10485760
    if value.size > limit:
        raise ValidationError("Please ensure that the size of your eula document is under 10MB.")
    else:
        return value


def validate_eula_file_type(value):
    """
    Set valid file types here, and in JS if applicable
    """
    ext = os.path.splitext(value.name)[1].lstrip('.')
    valid_extensions = ['doc', 'docx', 'html', 'pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Invalid file type for EULA. Must be one of: {}.".format(
            ', '.join(valid_extensions)
        ))
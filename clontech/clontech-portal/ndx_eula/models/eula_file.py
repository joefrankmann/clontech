from django.db import models
from django.utils.translation import ugettext_lazy as _

from ndx_eula.models.eula import Eula
from ndx_eula.models.validators import validate_eula_file_size, validate_eula_file_type, validate_language_code


class EulaFile(models.Model):
    eula = models.ForeignKey(
        Eula, related_name='eula_files', on_delete=models.CASCADE,
        blank=False, null=False)
    locale = models.CharField(
        _("Language code"),
        max_length=5,
        blank=False, null=False,
        help_text=_("For example: en, de, pt-BR"), validators=[validate_language_code])
    eula_file = models.FileField(
        upload_to='eula',
        blank=True, null=True,
        validators=[validate_eula_file_size, validate_eula_file_type])

    class Meta:
        ordering = ('locale',)
        unique_together = ('eula', 'locale')

    def __repr__(self):
        return 'EulaFile(pk={!r})'.format(self.pk)

    def __str__(self):
        return 'Eula File ({}) for "{}"'.format(self.locale, self.eula)

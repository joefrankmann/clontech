from logging import getLogger

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _, ugettext_noop

logger = getLogger()


class EulaQueryset(models.QuerySet):
    _logger = logger.getChild('EulaQueryset')

    def active(self):
        return self.filter(is_active=True)

    def past(self):
        now = timezone.now()
        self._logger.debug('past: Filtering for valid_from <= %s', now)
        return self.filter(valid_from__lte=timezone.now())


class Eula(models.Model):
    valid_from = models.DateTimeField(
        blank=False, null=False, auto_now_add=False, default=timezone.now,
        help_text=_("Only the latest EULA is shown to users. Future dates possible."))
    is_active = models.BooleanField(help_text=_("If not set, this Eula will not be shown to users."))

    objects = models.Manager.from_queryset(EulaQueryset)()

    class Meta:
        get_latest_by = 'valid_from'
        ordering = ('-valid_from',)

    def __repr__(self):
        return 'Eula(pk={!r})'.format(self.pk)

    def __str__(self):
        return 'Eula from {} ({})'.format(self.valid_from, _("active") if self.is_active else _("inactive"))

    def get_absolute_url(self):
        return reverse('ndx_eula:eula-detail', kwargs={'pk': self.pk})

    @property
    def is_valid_from_in_future(self):
        return self.valid_from > timezone.now()

    def locales(self):
        """Return the attached EulaFile's locales."""
        return (ef.locale for ef in self.eula_files.all())

    @property
    def status(self):
        """Return the status (active or inactive) as a string."""
        active = ugettext_noop("active")
        inactive = ugettext_noop("inactive")
        if self.is_active:
            return active
        return inactive

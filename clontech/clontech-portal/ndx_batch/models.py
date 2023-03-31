import datetime
from typing import Union

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _, ugettext_noop


class BatchQueryset(models.QuerySet):
    def active(self, when: Union[datetime.date, str]=None) -> models.QuerySet:
        if when is None:
            when = datetime.date.today()
        return self.filter(is_active=True, expires__gte=when, valid_from__lte=when)


class Batch(models.Model):
    TYPE_QUADRATIC = '2'
    TYPE_CHOICES = ((TYPE_QUADRATIC, _("quadratic")),)

    lot_no = models.CharField(_("Lot number"), max_length=127, blank=False, null=False, unique=True)
    assay_type = models.CharField(_("Assay type"), max_length=64, blank=False, null=False, 
                                  default=settings.NDX_BLANK_LEGACY_PLACEHOLDER)
    unit = models.CharField(_("Units"), max_length=64, blank=False, null=False)
    valid_from = models.DateField(_("Manufacture date"), blank=False, null=False, default=datetime.date.today)
    expires = models.DateField(blank=False, null=False)
    is_active = models.BooleanField(help_text=_("Whether this batch is visible to users."))
    curve_type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=TYPE_QUADRATIC)

    data_matrix_height = models.PositiveIntegerField(blank=True, null=True)
    data_matrix_width = models.PositiveIntegerField(blank=True, null=True)
    data_matrix = models.ImageField(
        upload_to='batch/lot_no', height_field='data_matrix_height', width_field='data_matrix_width',
        blank=True, null=False)

    comments = models.TextField(_("Comments"), null=True, blank=True)

    objects = models.Manager.from_queryset(BatchQueryset)()

    class Meta:
        get_latest_by = 'valid_from'
        ordering = ('-valid_from',)
        verbose_name = ("Batch")
        verbose_name_plural = _("Batches")

    def __repr__(self) -> str:
        return 'Batch(pk={!r})'.format(self.pk)

    def __str__(self) -> str:
        return '{}'.format(self.lot_no)

    @property
    def display_as_active(self) -> bool:
        return self.is_active and self.valid_from <= datetime.date.today() <= self.expires

    def get_absolute_url(self) -> str:
        return reverse('ndx_batch:batch', kwargs={'pk': self.pk})

    def is_expired(self) -> bool:
        return self.expires <= datetime.date.today()

    def is_valid_from_in_future(self) -> bool:
        return self.valid_from > datetime.date.today()

    @property
    def status(self) -> str:
        """Either "active" or "inactive", depending on whether the Batch is active and valid.

        This text is not translated so it can be used for CSS classes and such.
        """
        return ugettext_noop("active") if self.display_as_active else ugettext_noop("inactive")


class QuadraticCurveParameters(models.Model):
    batch = models.OneToOneField(
        Batch, primary_key=True, blank=False, null=False,
        on_delete=models.CASCADE,
        related_name='quadratic_curve_parameters')
    a = models.FloatField(_("2nd degree coefficient"), blank=False, null=False)
    b = models.FloatField(_("1st degree coefficient"), blank=False, null=False)
    c = models.FloatField(_("Constant offset"), blank=False, null=False)

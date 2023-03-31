from ndx_result_source.models.result import *  # noqa
import ndx_result_source.models.result as source  # noqa

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

from ndx_django_utils.models.fields import CSVJSONField


class Result(source.Result):
    INTERPRETATION_POSITIVE = 'Valid'
    INTERPRETATION_OLD_POSITIVE = 'Positive'
    INTERPRETATION_NEGATIVE = 'Negative'
    INTERPRETATION_INVALID = 'Invalid'
    INTERPRETATION_OFFSCALE = 'OffScale'
    INTERPRETATION_CHOICES = (
        (INTERPRETATION_POSITIVE, _("Valid")),
        (INTERPRETATION_OLD_POSITIVE, _("Positive")),
        (INTERPRETATION_NEGATIVE, _("Negative")),
        (INTERPRETATION_INVALID, _("Invalid")),
        (INTERPRETATION_OFFSCALE, _("OffScale"))
    )

    uploader_email = models.EmailField(
        _("Uploader Email"), max_length=255, blank=True, null=False, default=settings.NDX_BLANK_LEGACY_PLACEHOLDER,
        help_text=_('tester email address'))
    batch = models.ForeignKey(
        'ndx_batch.Batch', on_delete=models.PROTECT,
        verbose_name=_("Lot No."), blank=False, null=True)
    notes = models.TextField(_("Notes"), blank=True, null=False, default="")

    assay_type = models.CharField(
        _("Assay type"), max_length=64, blank=False, null=False, default=settings.NDX_BLANK_LEGACY_PLACEHOLDER)
    dilution = models.CharField(_("Dilution"), max_length=64, default="1:1")
    sample_name = models.CharField(
        _("Sample name"), max_length=128, blank=True, null=False, default=settings.NDX_BLANK_LEGACY_PLACEHOLDER)
    is_reference = models.BooleanField(
        _("Reference sample?"),
        blank=True, null=False, default=False)
    reference_name = models.CharField(
        _("Reference name"), max_length=128, blank=True, null=False, default="",
        help_text=_("Name of this sample (for reference samples)"))
    unit = models.CharField(
        _("Unit"), max_length=64, blank=True, null=False, default="",
        help_text=_("Unit (for reference samples)"))
    titre = models.FloatField(
        _("Titre"), blank=True, null=False, default=0,
        help_text=_("Titre (for reference samples)"))
    gostix_value = models.FloatField(
        _("GoStix Value"), blank=True, null=False, default=0)

    interpretation = models.CharField(
        _("Interpretation"), max_length=len('positive'), blank=False, null=False,
        choices=INTERPRETATION_CHOICES, default=INTERPRETATION_INVALID)
    generated_csv_row = CSVJSONField(null=True, blank=True)

    location = None
    device_display_name = None

    class Meta:
        get_latest_by = 'created_at'
        ordering = ('-created_at',)
        permissions = (
            ('view_result', _("Can view results")),
            ('view_all_results', _("View all results")),
            ('view_qc_results', _("View QC results")),
            ('view_own_result', _("View own result")),
        )

    @property
    def overall_outcome(self) -> str:
        if self.interpretation == 'OffScale':
            return 'Off Scale'
        return self.interpretation

    @property
    def individual_interpretations(self):
        raise NotImplementedError("This is a single interpretation model.")
    
    @classmethod
    def get_csv_headers(cls) -> [(str, str)]:
        """
        These tuples correspond to csv header fields (left), and the actual attribute path for this value (right). Using this
        implementation allows us to ensure consistency between headers and values.
        """
        return [("analysis_type", "analysis_type"), 
                ("app_version", "app_version"),
                ("assay_type", "assay_type"),
                ("average_iteration_time", "average_iteration_time"),
                ("batch", "batch"),
                ("batch.curve_type", "batch.curve_type"),
                ("batch.expires", "batch.expires"),
                ("batch.is_active", "batch.is_active"),
                ("batch.valid_from", "batch.valid_from"),
                ("created_at", "created_at"),
                ("device_id", "device_id"),
                ("device_make", "device_make"),
                ("device_model", "device_model"),
                ("device_os", "device_os"),
                ("dilution", "dilution"),
                ("first_occurrence_of_green_time", "first_occurrence_of_green_time"),
                ("first_occurrence_of_yellow_time", "first_occurrence_of_yellow_time"),
                ("geo_location", "geo_location"),
                ("geo_location.latitude", "geo_location.latitude"),
                ("geo_location.longitude", "geo_location.longitude"),
                ("gostix_value", "gostix_value"),
                ("interpretation", "interpretation"),
                ("is_reference", "is_reference"),
                ("notes", "notes"),
                ("reader_type", "reader_type"),
                ("reader_version", "reader_version"),
                ("reference_name", "reference_name"),
                ("sample_id", "sample_id"),
                ("sample_name", "sample_name"),
                ("teststrip.baseline", "teststrips.baseline"),
                ("teststrip.cline_peak_position", "teststrips.cline_peak_position"),
                ("teststrip.cline_score", "teststrips.cline_score"),
                ("teststrip.image", "teststrips.image"),
                ("teststrip.profile", "teststrips.profile"),
                ("teststrip.t_c_ratio", "teststrips.tlines.t_c_ratio"),
                ("teststrip.tline_peak_position", "teststrips.tlines.peak_position"),
                ("teststrip.tline_score", "teststrips.tlines.score"),
                ("titre", "titre"),
                ("transition_to_result_time", "transition_to_result_time"),
                ("unit", "unit"),
                ("created_by", "created_by"),
                ("uploader_email", "uploader_email")]

    fields_to_hide_for_qc = ['created_by', 'uploader_email']

    @property
    def has_csv_data(self):
        row_data = self.generated_csv_row
        return row_data and row_data != {}

    def generate_csv_row(self) -> dict:
        row = {}
        for entry in self.get_csv_headers():
            row[entry[0]] = str(recursive_getattr(self, entry[1]))
        return row

    def save_csv_row(self) -> None:
        self.generated_csv_row = self.generate_csv_row()
        self.save()


def recursive_getattr(obj, attr, default=""):
    """
    Recursive wrapper over getattr to allow multiple layers of attributes to be loaded (i.e. teststrips.tlines.t_c_ratio).
    This implementation is opinionated and intended for this specific use case, it should not be used elsewhere without
    careful consideration.
    """
    attrs = attr.split('.')
    value = getattr(obj, attrs[0], None)
    if attrs[0] in ['teststrips', 'tlines'] and value is not None:
        value = value.first()
    # essentially, if the attribute doesn't exist
    if value is None:
        # we can return the default "" here as if any part of the requested attr doesn't exist, it is an empty entry in the csv
        return default
    elif len(attrs[1:]) > 0:
        new_attr = '.'.join(attrs[1:])
        return recursive_getattr(value, new_attr, default=default)
    else:
        return value


@receiver(post_save, sender=Result, dispatch_uid="ndx_result_generate_csv")
def generate_csv_row(sender, instance, created, update_fields, **kwargs):
    # crucial that it doesn't update when "generated_csv_row" hasn't been updated, otherwise it will recurse
    if created or (update_fields and "generated_csv_row" not in update_fields):
        instance.save_csv_row()

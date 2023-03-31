from ndx_result_source.apps import *  # noqa
import ndx_result_source.apps as source  # noqa

from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def setup_clontech_permissions(sender, **kwargs):
    from ndx_portal.migration_utils import set_group_permissions
    set_group_permissions('administrators', ['view_all_results', 'view_own_result', 'view_result', 'view_qc_results'])
    set_group_permissions('qc user', ['view_qc_results', 'view_own_result', 'view_result'])


def generate_all_csv_rows(sender, **kwargs):
    from ndx_result.models import Result
    print('Generating csv row data for every result. This may take a while.')
    for result in Result.objects.all():
        if not result.has_csv_data:
            result.save_csv_row()


def fix_blank_legacy_fields(sender, **kwargs):
    from ndx_result.models import Result
    legacy_attrs = ['uploader_email', 'assay_type', 'sample_name']
    for result in Result.objects.all():
        for attr in legacy_attrs:
            if str(getattr(result, attr)).strip() in ('', 'None'):
                setattr(result, attr, settings.NDX_BLANK_LEGACY_PLACEHOLDER)
        result.save()


class NdxResultConfig(AppConfig):
    """AppConfig for the NdxResult app"""

    name = "ndx_result"
    verbose_name = "Ndx Result"

    def ready(self):
        post_migrate.connect(source.setup_user_levels, sender=self)
        post_migrate.connect(setup_clontech_permissions, sender=self)
        post_migrate.connect(fix_blank_legacy_fields, sender=self)
        post_migrate.connect(generate_all_csv_rows, sender=self)

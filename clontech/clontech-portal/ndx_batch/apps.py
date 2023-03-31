from django.apps import AppConfig
from django.conf import settings
from django.db.models.signals import post_migrate


def setup_clontech_permissions(sender, **kwargs):
    from ndx_portal.migration_utils import set_group_permissions
    set_group_permissions('administrators', ['add_batch', 'change_batch'])
    set_group_permissions('qc user', ['add_batch', 'change_batch'])


def fix_assay_types(sender, **kwargs):
    from ndx_batch.models import Batch
    for batch in Batch.objects.all():
        if batch.assay_type.strip() == '' or batch.assay_type == 'test_assay_1':
            batch.assay_type = settings.NDX_BLANK_LEGACY_PLACEHOLDER
            batch.save()


class NdxBatchConfig(AppConfig):
    name = 'ndx_batch'
    verbose_name = "Batch Management"

    def ready(self):
        from . import signals  # noqa
        post_migrate.connect(setup_clontech_permissions, sender=self)
        post_migrate.connect(fix_assay_types, sender=self)

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def setup_clontech_permissions(sender, **kwargs):
    from ndx_portal.migration_utils import set_group_permissions
    set_group_permissions('administrators', ['add_eula', 'change_eula'])
    set_group_permissions('qc user', ['add_eula', 'change_eula'])


class NdxEulaConfig(AppConfig):
    name = 'ndx_eula'
    verbose_name = "EULA"

    def ready(self):
        post_migrate.connect(setup_clontech_permissions, sender=self)

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def setup_clontech_permissions(sender, **kwargs):
    from ndx_portal.migration_utils import set_group_permissions
    set_group_permissions('administrators', ['view_feedback'])
    set_group_permissions('mobile app', ['add_feedback'])


class NdxFeedbackConfig(AppConfig):
    name = "ndx_feedback"
    verbose_name = "User Feedback Management"

    def ready(self):
        from ndx_feedback import signals  # noqa
        post_migrate.connect(setup_clontech_permissions, sender=self)

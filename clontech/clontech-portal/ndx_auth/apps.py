from django.conf import settings
from django.db import transaction
from ndx_auth_source.apps import *  # noqa
import ndx_auth_source.apps as source  # noqa

from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.db.models.signals import post_migrate


def setup_clontech_permissions(sender, **kwargs):
    from ndx_portal.migration_utils import set_group_permissions
    set_group_permissions('administrators', ['change_ndxuser', 'view_all_users',
                                             'edit_all_users', 'view_user_data', 'change_feedback_emails'])


def ensure_mobile_user_exists(sender, **kwargs):
    """
    Creates the mobile user and ensures it belongs to the correct group.
    If the user does not exist, it attempts to create it using the environment variable: 

        NDX_MOBILE_USER_PASSWORD

    On the server you should set this in envdir. Locally you can prefix the management command:
        
        NDX_MOBILE_USER_PASSWORD=xyz ./manage.py migrate

    """
    from ndx_auth.models import NdxUser, UserType
    from django.contrib.auth.models import Group
    
    mobile_user_email = settings.NDX_MOBILE_USER_EMAIL
    password = settings.NDX_MOBILE_USER_PASSWORD
    
    with transaction.atomic():
        # Ensure Group exists
        Group.objects.get_or_create(name='mobile app')
        # Ensure user exists..
        try:
            mobile_app_user = NdxUser.objects.get(email=mobile_user_email)
        except NdxUser.DoesNotExist:
            if password is None:
                raise ImproperlyConfigured('Setting NDX_MOBILE_USER_PASSWORD is required to create mobile user account.')
            mobile_app_user = NdxUser.objects.create_user(
                name='Novarum Mobile App',
                email=mobile_user_email,
                password=password
            )
        mobile_app_user.update_user_type(UserType.MOBILE_APP)


class NdxAuthConfig(AppConfig):
    """AppConfig for the NdxAuth app"""

    name = "ndx_auth"
    verbose_name = "Ndx Auth"

    def ready(self):
        """Run code when Django has finished loading apps"""
        post_migrate.connect(source.setup_user_levels, sender=self)
        post_migrate.connect(setup_clontech_permissions, sender=self)
        post_migrate.connect(ensure_mobile_user_exists, sender=self)

from ndx_auth_source.models.user_type import *  # noqa
import ndx_auth_source.models.user_type as source  # noqa

from django.conf import settings


class UserType(source.UserTypeEnumMixin, source.Enum):
    """
    The type of a user as reflected in its groups.
    The ordering of these is extremely important, a user in a group will also be in *every* group below that in this enum.
    i.e. a QC_USER will also be in the USER group and a SUPERUSER will be in every group.

    We don't use ORGANISATION_ADMIN or USER in this portal (but we need to keep them or shadow apps breaks)
    """
    SUPERUSER = ('superuser', False, None, 'superuser')
    ADMIN = ('administrators', True, 'administrators', settings.NDX_USER_TYPES_ADMIN_GROUP_NAME)
    ORGANISATION_ADMIN = ('organisation_administrators', True, 'organisation_administrators',
                          'Organisation Administrator')
    USER = ('users', True, 'users', settings.NDX_USER_TYPES_USER_GROUP_NAME)
    QC_USER = ('qc user', True, 'qc user', 'QC User')
    MOBILE_APP = ('mobile', True, 'mobile app', 'Mobile App')
    
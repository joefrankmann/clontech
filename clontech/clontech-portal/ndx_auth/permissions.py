from ndx_auth_source.permissions import *  # noqa
import ndx_auth_source.permissions as source  # noqa


class NdxUserPermission(source.PermissionEnum):
    """User permissions.

    The following permissions are defined:
        ADD: Create a user
        CHANGE: Edit a user
        DELETE: Delete a user
        VIEW: View a user
        VIEW_ALL_ORGS: View all organisations
        CHANGE_PASSWORD: Change a user's password
    """
    ADD = 'ndx_auth.add_ndxuser'
    CHANGE = 'ndx_auth.change_ndxuser'
    DELETE = 'ndx_auth.delete_ndxuser'
    VIEW = 'ndx_auth.view_ndxuser'
    VIEW_ALL_ORGS = 'ndx_auth.view_all_orgs'
    CHANGE_PASSWORD = 'ndx_auth.change_ndxuser_password'
    EDIT_ALL_USERS = 'ndx_auth.edit_all_users'
    VIEW_ALL_USERS = 'ndx_auth.view_all_users'
    VIEW_USER_DATA = 'ndx_auth.view_user_data'
    CHANGE_FEEDBACK_EMAILS = "ndx_auth.change_feedback_emails"

"""
This file should not be used anywhere except in the fix_groups management command.

Old clontech:

    - A QC user is determined by whether it belongs to group 'qc user' (they might belong to other groups too).
    - Admin group is called 'portal admin'
    
New clontech:

    - An admin would automatically belong to group 'qc user' (because it's lower than admin in the enum, its how 
      shadow apps does it)
    - Admin group is called 'portal admin'

"""
from django.contrib.auth.models import Group
from ndx_auth.models import NdxUser, UserType


def fix_group_names():
    """
    Moves users to correct groups, deletes unused old admin group, and sets potentially
    missing group permissions.
    """
    # Set users to correct UserTypes & groups
    for user in NdxUser.objects.all():
        if user.is_superuser:
            user.update_user_type(UserType.SUPERUSER)
        elif user.groups.filter(name='portal admin').exists():
            user.update_user_type(UserType.ADMIN)
        elif user.groups.filter(name='qc user').exists():
            user.update_user_type(UserType.QC_USER)
        elif user.groups.filter(name='mobile user').exists():
            user.update_user_type(UserType.MOBILE_USER)
        else:
            try:
                user_type = UserType.get(user).codename
            except ValueError:
                user_type = 'no type'
            print('Unexpected usertype {} {}'.format(user, user_type))

    # Delete old admin group (should have no more members)
    try:
        Group.objects.get(name='portal admin').delete()
    except Group.DoesNotExist:
        pass
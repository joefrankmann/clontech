"""
Utility functions for post_migrate.connect() actions.
You cannot import models at top level as apps will not be ready by that point.
Import inside functions instead.
"""


def set_group_permissions(group, permissions):
    """
    @permissions must be iterable of codenames
    """
    from django.contrib.auth.models import Group, Permission
    group, created = Group.objects.get_or_create(name=group)
    for codename in permissions:
        permission = Permission.objects.get(codename=codename)
        group.permissions.add(permission)
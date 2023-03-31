from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

User = get_user_model()


class GroupPermissionsTestCase(TestCase):
    PORTAL_ADMIN_PERMISSIONS = (
        'ndx_result.view_own_result',
        'ndx_result.view_qc_results',
        'ndx_result.view_all_results',
        'ndx_batch.add_batch',
        'ndx_batch.change_batch',
        'ndx_eula.add_eula',
        'ndx_eula.change_eula',
        'ndx_auth.add_ndxuser',
        'ndx_auth.change_ndxuser',
        'ndx_auth.view_all_users',
        'ndx_auth.edit_all_users',
        'ndx_auth.change_feedback_emails'
    )
    QC_PERMISSIONS = (
        'ndx_result.view_qc_results',
        'ndx_batch.change_batch',
        'ndx_eula.add_eula',
        'ndx_eula.change_eula',
    )

    def test_portal_admin_group_has_permissions(self):
        group = Group.objects.get(name='administrators')
        user = User.objects.create()
        user.groups.set((group,))
        for permspec in self.PORTAL_ADMIN_PERMISSIONS:
            self.assertTrue(user.has_perm(permspec), permspec)

    def test_qc_group_has_permissions(self):
        group = Group.objects.get(name='qc user')
        user = User.objects.create()
        user.groups.set((group,))
        for permspec in self.QC_PERMISSIONS:
            self.assertTrue(user.has_perm(permspec), permspec)

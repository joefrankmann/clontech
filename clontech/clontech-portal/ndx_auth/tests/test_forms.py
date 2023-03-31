from ndx_auth_source.tests.test_forms import *  # noqa
import ndx_auth_source.tests.test_forms as source  # noqa

from ndx_auth.models import NdxUser


class UserFormTestCase(source.UserFormTestCase):
    """
    We don't use organisations, and form has an additional field.
    """
    def test_user_is_not_in_organisation_by_default(self):
        pass

    def test_user_is_in_organisation_when_passed_organisation(self):
        pass

    def test_user_does_not_receive_feedback_by_default(self):
        user = NdxUser.objects.create_user(email='a@localhost', password='pw', name='n')
        self.assertFalse(user.feedback_emails)

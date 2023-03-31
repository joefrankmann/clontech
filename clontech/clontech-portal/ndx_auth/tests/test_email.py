from ndx_auth_source.tests.test_email import *  # noqa
import ndx_auth_source.tests.test_email as source  # noqa

from ndx_auth.models import NdxUser, UserType


class UserFormTestCase(source.UserFormTestCase):
    """
    We have to create a proper user or else the qc_user dropdown in the form is empty,
    and seeing the field is required we get an error saying:
    
        "ValueError: The NdxUser could not be created because the data didn't validate."

    """
    @classmethod
    def setUpTestData(cls):
        cls.request = RequestFactory().get('/')
        user = NdxUser.objects.create_user(email='a@localhost', password='pw', name='n')
        user.update_user_type(UserType.ADMIN)
        cls.request.user = user

    @classmethod
    def make_user(cls):
        form = UserForm(
            request=cls.request, 
            data={
                'email': "novarumuser@localhost.com",
                'name': "Connie",
                'feedback_emails': False,
                'user_type': "administrators"
            }, 
            user_type=UserType.ADMIN
        )
        return form.save()

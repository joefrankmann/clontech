from ndx_result_source.tests.test_views import *  # noqa
import ndx_result_source.tests.test_views as source  # noqa

from django.test import TestCase, RequestFactory

from ndx_auth.models import UserType, NdxUser
from ndx_result.api_views import generate_filters


class ResultsCSVDownladTestCase(TestCase):
    """
    This tests that the method 'generate_filters()' applies a correction to the date range filter kwargs.
    Results created on a given day will have a respective time of creation for which will make that objects 
    'created_at' time be greater than the start of that day. 
    Therefore for the filter to be inclusive of Results created at any time on the user selected 'end_date', 
    the method 'generate_filters()' extends the 'create_at__lt' value by 1 day thereby including all results 
    up until the start of the following day.
    """

    @classmethod
    def setUpTestData(cls):
        cls.normal_user = NdxUser(email='normal@test.test')
        cls.normal_user.set_password('secret')
        cls.normal_user.save()
        cls.normal_user.update_user_type(UserType.USER)
    
    def test_filters_date_range(self):
        end_date = '2020-02-20'
        get_string = '/api/result/csv?end_date={}'.format(end_date) 
        self.request = RequestFactory().get(get_string)
        self.request.user = self.normal_user
        
        filter_kwargs = generate_filters(self.request)
        self.assertEqual(filter_kwargs.get('created_at__lt'), '2020-02-21')

import datetime
from django.test import TestCase

from ..forms import BatchForm


class BatchFormTestCase(TestCase):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    last_week = today - datetime.timedelta(days=7)

    def test_valid_form_is_valid(self):
        data = {'lot_no': '123', 'assay_type': "test", 'unit': "mg/l",
                'valid_from': str(self.today), 'expires': str(self.tomorrow), 'is_active': True, 'comments': "test"}
        form = BatchForm(data)
        self.assertTrue(form.is_valid())

    def test_form_comments_can_be_empty(self):
        data = {'lot_no': '123', 'assay_type': "test", 'unit': "mg/l",
                'valid_from': str(self.today), 'expires': str(self.tomorrow), 'is_active': True}
        form = BatchForm(data)
        self.assertTrue(form.is_valid())

    def test_expiry_must_be_after_valid_from(self):
        data = {'lot_no': '123', 'assay_type': "test", 'unit': "mg/l",
                'valid_from': str(self.tomorrow), 'expires': str(self.today), 'is_active': True, 'comments': "test"}
        form = BatchForm(data)
        self.assertFalse(form.is_valid())

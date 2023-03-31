from django.test import TestCase
from ndx_feedback.models import Feedback

import json
import os


class FeedbackTestCase(TestCase):
    @classmethod
    def setUpTestData(self):
        self.feedback_data = json.load(open(os.path.join(os.path.dirname(__file__), "feedback_body.json")))
        feedback = Feedback(**self.feedback_data)
        feedback.save()

    def setUp(self):
        self.feedback = Feedback.objects.get()

    def test_properties(self):
        # device and reader are not database field, they are class properties generated from various other fields
        # however several things rely on them, as such it should be checked that they are formed correctly
        expected_device = " ".join([self.feedback.device_os, self.feedback.device_make, self.feedback.device_model])
        self.assertEqual(self.feedback.device, expected_device)

        expected_reader = " ".join([self.feedback.reader_type, self.feedback.reader_version])
        self.assertEqual(self.feedback.reader, expected_reader)

    def test_values(self):
        # check that each model field was saved as expected
        for key in self.feedback_data.keys():
            self.assertEqual(
                getattr(self.feedback, key),
                self.feedback_data[key],
                msg="Field {} was not saved correctly".format(key)
            )

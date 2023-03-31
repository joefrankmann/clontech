from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from ndx_auth.models import NdxUser
from ndx_feedback.models import Feedback

import json
import os


class FeedbackCSVTestCase(APITestCase):

    @classmethod
    def setUpTestData(self):
        user = NdxUser(email='a@b.c', is_superuser=True)
        user.set_password('secret')
        user.save()
        feedback_data = json.load(open(os.path.join(os.path.dirname(__file__), "feedback_body.json")))
        feedback = Feedback(**feedback_data)
        feedback.save()

    def setUp(self):
        self.client.login(username="a@b.c", password="secret")
        self.url = reverse("ndx_feedback_api:feedback_csv")

    def tearDown(self):
        self.client.logout()

    def test_csv_row_generation_on_record(self):
        feedback_record = Feedback.objects.all().first()
        csv_data = feedback_record.csv_row
        headers = Feedback.get_csv_headers()
        for i, pair in enumerate(Feedback.csv_fields):
            name, prop = pair
            expected_cell_value = str(getattr(feedback_record, prop))
            self.assertEqual(csv_data[i], expected_cell_value,
                             msg="Field {} was not entered correctly in the csv".format(name))

    def test_csv_api(self):
        response = self.client.get(reverse('ndx_feedback_api:feedback_csv'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("Content-Type"), "text/csv")
        # check that the Content-Disposition header is along the lines of
        # attachment; filename="feedback_results_2019-11-27T18:01:15.390028+00:00.csv"
        self.assertRegex(response.get("Content-Disposition"), r'attachment; filename="feedback_results_.*\.csv"')
        csv_rows = []
        for i in response.streaming_content:
            csv_rows.append(i)
        # The first row of the csv should be the headers, followed by a carriage return line break which must be stripped
        header_row = csv_rows[0].decode('utf-8').strip('\r\n').split(',')
        # As there is only 1 Feedback entry, the 2nd row contains the information relating to this
        content_row = csv_rows[1].decode('utf-8').strip('\r\n').split(',')
        # Get model information to ensure that the returned information matches what is saved in the database
        headers = Feedback.get_csv_headers()
        feedback_record = Feedback.objects.all().first()
        self.assertEqual(headers, header_row)


        for i, pair in enumerate(Feedback.csv_fields):
            name, prop = pair
            expected_cell_value = str(getattr(feedback_record, prop))
            self.assertEqual(content_row[i], expected_cell_value,
                             msg="Field {} was not entered correctly in the csv".format(name))

from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import Permission
from django.urls import reverse

import os
import json


from ndx_auth.models import NdxUser
from ndx_feedback.models import Feedback


class FeedbackAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(self):
        user = NdxUser(email='a@b.c', is_superuser=True)
        user.set_password('secret')
        user.save()

    def setUp(self):
        self.client.login(username="a@b.c", password="secret")
        self.url = reverse("ndx_feedback_api:feedback-list")
        self.feedback_data = json.load(open(os.path.join(os.path.dirname(__file__), "feedback_body.json")))

    def tearDown(self):
        self.client.logout()

    def test_user_can_post_data(self):
        original_feedback_count = Feedback.objects.count()
        response = self.client.post(self.url, self.feedback_data)
        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED, msg=response.content)
        # Check that 1 feedback object was created
        self.assertEqual(Feedback.objects.count() - original_feedback_count, 1)

        # Check that all values were saved into the database correctly
        feedback = Feedback.objects.get(pk=content['id'])
        for field in self.feedback_data.keys():
            self.assertEqual(getattr(feedback, field, None),
                             self.feedback_data[field], msg="field {} was not saved correctly".format(field))

    def test_user_can_get_data(self):

        feedback = Feedback(**self.feedback_data)
        feedback.save()

        response = self.client.get(self.url)
        self.assertTrue(response.status_code, status.HTTP_200_OK)

        content = json.loads(response.content.decode('utf-8'))
        self.assertEqual(content["count"], Feedback.objects.count())

        for result in content["results"]:
            feedback = Feedback.objects.get(pk=result["id"])
            for field in result.keys():
                # created is returned as a datetime object so isn't equal even if the data is correct
                if field != "created_at":
                    self.assertEqual(getattr(feedback, field, None),
                                     result[field], msg="field {} was not returned correctly".format(field))

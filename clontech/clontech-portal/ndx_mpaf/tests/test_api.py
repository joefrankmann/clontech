from unittest.mock import MagicMock
import os
import json

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

IMAGE_B64_FILE = os.path.join(os.path.dirname(__file__), 'strip_image.b64')
NDX_RESULT_JSON_FILE = os.path.join(os.path.dirname(__file__), 'result-full-1strip-image.json')
MINIMAL_RESULT_JSON_FILE = os.path.join(os.path.dirname(__file__), 'minimal_result.json')


class NdxResultApiTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        user = User(email='a@b.c')
        user.set_password('secret')
        user.save()
        user.user_permissions.add(Permission.objects.get(content_type__model='result', codename='add_result'))

    def setUp(self):
        self.client.login(username='a@b.c', password='secret')
        self.create_url = reverse('mpaf-api:result-list')

    def tearDown(self):
        self.client.logout()

    def test_submit_mpaf_result(self):
        image_data = open(IMAGE_B64_FILE).read()
        results_data = json.load(open(NDX_RESULT_JSON_FILE))
        result = results_data['results'][0]
        teststrips = result['TestStrips'][:2]
        for teststrip in teststrips:
            teststrip['StripImageBase64'] = image_data
        result['TestStrips'] = teststrips
        response = self.client.post(self.create_url, {'results': (result,)})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.content)
        self.assertTrue(response.data['results'])

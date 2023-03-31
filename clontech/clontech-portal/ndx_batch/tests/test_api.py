from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.db import transaction

from ndx_auth.models import NdxUser
from ndx_batch.models import Batch

from freezegun import freeze_time


class BatchAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(self):
        user = NdxUser(email='a@b.c', is_superuser=True)
        user.set_password('secret')
        user.save()

        active_batch = Batch(lot_no="test_active", valid_from="2003-01-01", expires="2019-01-01", is_active=True)
        active_batch.save()

        inactive_batch = Batch(lot_no="test_inactive", valid_from="2000-01-01", expires="2018-01-01", is_active=False)
        inactive_batch.save()

    def setUp(self):
        self.client.login(username="a@b.c", password="secret")
        self.url = reverse("ndx-batch-api:batches-active")

    def tearDown(self):
        self.client.logout()

    def test_endpoint_returns_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_endpoint_returns_active(self):
        with freeze_time("2017-01-01 06:00:00"):
            response = self.client.get(self.url)
            self.assertEqual(response.data["count"], 1)
            self.assertEqual(response.data["count"], len(response.data["results"]))

    def test_endpoint_doesnt_return_after_expiry(self):
        with freeze_time("2020-01-01 06:00:00"):
            response = self.client.get(self.url)
            self.assertEqual(response.data["count"], 0)
            self.assertEqual(len(response.data["results"]), 0)

    def test_endpoint_doesnt_return_before_valid(self):
        with freeze_time("2002-01-01 06:00:00"):
            response = self.client.get(self.url)
            self.assertEqual(response.data["count"], 0)
            self.assertEqual(len(response.data["results"]), 0)




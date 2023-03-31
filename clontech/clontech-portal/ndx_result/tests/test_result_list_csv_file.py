from ndx_result_source.tests.test_result_list_csv_file import *  # noqa
import ndx_result_source.tests.test_result_list_csv_file as source  # noqa

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from django.contrib.auth.models import Group
from ndx_auth.models import UserType, NdxUser

from ndx_result.models.result import Result, recursive_getattr

import json
import datetime


class ResultListCsvFileTestCase(APITestCase):
    """
    This tests the new method for CSV generation, which doesn't use use the ResultListCSVFile model, 
    but generates it on the fly instead. The name of this needs to stay the same though so as to 
    override the shadow apps one, additionally: it extends from APITestCase instead of the
    shadow apps test as they are 2 completely separate and different classes doing different things.
    """

    @classmethod
    def setUpTestData(cls):
        cls.superuser = NdxUser(email='su@test.test', is_superuser=True)
        cls.superuser.set_password('secret')
        cls.superuser.save()

        cls.qc_user = NdxUser(email='qc@test.test')
        cls.qc_user.set_password('secret')
        cls.qc_user.save()
        cls.qc_user.update_user_type(UserType.QC_USER)

        cls.qc_user2 = NdxUser(email='qc2@test.test')
        cls.qc_user2.set_password('secret')
        cls.qc_user2.save()
        cls.qc_user2.update_user_type(UserType.QC_USER)

        cls.administrator = NdxUser(email="admin@test.test")
        cls.administrator.set_password('secret')
        cls.administrator.save()
        cls.administrator.update_user_type(UserType.ADMIN)

        cls.normal_user = NdxUser(email='normal@test.test')
        cls.normal_user.set_password('secret')
        cls.normal_user.save()
        cls.normal_user.update_user_type(UserType.USER)

    def setUp(self):
        self.client.login(username="su@test.test", password="secret")

        with open('ndx_result/tests/result-full-1strip-image.json', 'r') as infile:
            self.client.post(reverse('mpaf-api:result-list'), json.load(infile), format='json')

    def test_api_returns_correct_headers(self):
        response = self.client.get(reverse("ct-result-api:api_result_csv"))
        lines = []
        for line in response.streaming_content:
            lines.append(line)
        self.assertEqual(2, len(lines))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual('application/csv', response.get('Content-Type'))
        self.assertRegex(response.get('Content-Disposition'), r'attachment; filename="results_.*\.csv"')

    def test_qc_user_only_sees_qc_results(self):
        self.client.force_login(user=self.qc_user)
        response = self.client.get(reverse("ct-result-api:api_result_csv"))
        lines = []
        for line in response.streaming_content:
            lines.append(line)
        # 1 line should remain, due to the csv headers
        self.assertEqual(len(lines), 1)
        Result.objects.create(created_by=self.qc_user, uploader_email="qc@test.test",
                              created_at=datetime.datetime.now())
        Result.objects.create(created_by=self.qc_user2, uploader_email="qc2@test.test",
                              created_at=datetime.datetime.now())
        response = self.client.get(reverse("ct-result-api:api_result_csv"))
        lines = []
        for line in response.streaming_content:
            lines.append(line)
        # Should only be able to see qc results
        self.assertEqual(len(lines), 3)

    def test_other_users_only_sees_own_results(self):
        self.client.force_login(user=self.normal_user)
        response = self.client.get(reverse("ct-result-api:api_result_csv"))
        lines = []
        for line in response.streaming_content:
            lines.append(line)
        # 1 line should remain, due to the csv headers
        self.assertEqual(len(lines), 1)
        Result.objects.create(created_by=self.qc_user, uploader_email="qc@test.test",
                              created_at=datetime.datetime.now())
        Result.objects.create(created_by=self.normal_user, uploader_email="normal@test.test",
                              created_at=datetime.datetime.now())
        response = self.client.get(reverse("ct-result-api:api_result_csv"))
        lines = []
        for line in response.streaming_content:
            lines.append(line)
        # Should only be able to see own results
        self.assertEqual(len(lines), 2)

    def test_administrator_can_see_all_results(self):
        self.client.force_login(self.administrator)
        # a result for the superuser is already added in setUp
        Result.objects.create(created_by=self.qc_user, uploader_email="qc@test.test",
                              created_at=datetime.datetime.now())
        Result.objects.create(created_by=self.normal_user, uploader_email="normal@test.test",
                              created_at=datetime.datetime.now())
        response = self.client.get(reverse("ct-result-api:api_result_csv"))
        lines = []
        for line in response.streaming_content:
            lines.append(line)
        # Should only be able to see all results + a header line
        self.assertEqual(len(lines), 4)

    def test_super_user_can_see_all_results(self):
        self.client.force_login(self.superuser)
        # a result for the superuser is already added in setUp
        Result.objects.create(created_by=self.qc_user, uploader_email="qc@test.test",
                              created_at=datetime.datetime.now())
        Result.objects.create(created_by=self.normal_user, uploader_email="normal@test.test",
                              created_at=datetime.datetime.now())
        response = self.client.get(reverse("ct-result-api:api_result_csv"))
        lines = []
        for line in response.streaming_content:
            lines.append(line)
        # Should only be able to see all results + a header line
        self.assertEqual(len(lines), 4)

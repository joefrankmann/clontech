import http.client

from django.contrib.auth.models import Permission
from django.test import TestCase, Client
from django.urls import reverse

from ndx_auth.models import NdxUser, UserType
from ndx_feedback.models import Feedback


PASSWORD = 'test'


def create_user(email, user_type):
    user = NdxUser.objects.create_user(name='not joe',email=email, password=PASSWORD)
    user.update_user_type(user_type)
    return user


class FeedbackViewTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.feedback = Feedback.objects.create(
            uploader_email="tester@test.com",
            device_os="1.0.0",
            device_make="huawei",
            device_model="p20",
            device_id="123456",
            app_version="1.0.0",
            reader_type="test",
            reader_version="1.0.0",
            rating="good",
            follow_up=False,
            comments="I love this app."
        )
        cls.normal_user = create_user('normal@example.com', UserType.ADMIN)
        cls.qc_user = create_user('qc_user@example.com', UserType.QC_USER)
        cls.client = Client()

    def test_normal_user_can_access_views(self):
        self.client.login(username=self.normal_user.email, password=PASSWORD)
        response = self.client.get(reverse('ndx_feedback:feedback'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('ndx_feedback:feedback-detail', kwargs={'pk': self.feedback.id}))
        self.assertEqual(response.status_code, 200)

    def test_qc_user_cannot_access_views(self):
        self.client.login(username=self.qc_user.email, password=PASSWORD)
        response = self.client.get(reverse('ndx_feedback:feedback'))
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('ndx_feedback:feedback-detail', kwargs={'pk': self.feedback.id}))
        self.assertEqual(response.status_code, 302)

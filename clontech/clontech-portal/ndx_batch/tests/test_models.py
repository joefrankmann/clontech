import datetime
from django.test import TestCase
from freezegun import freeze_time

from ..models import Batch


class BatchQuerysetTestCase(TestCase):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    last_week = today - datetime.timedelta(days=7)

    def test_active_returns_only_active_batches(self):
        Batch.objects.create(lot_no='1', is_active=True, valid_from=self.last_week, expires=self.today)
        Batch.objects.create(lot_no='2', is_active=True, valid_from=self.last_week, expires=self.today)
        Batch.objects.create(lot_no='3', is_active=False, valid_from=self.last_week, expires=self.today)

        active_batches = Batch.objects.active()
        self.assertTrue(active_batches.filter(lot_no='1').exists())
        self.assertTrue(active_batches.filter(lot_no='2').exists())
        self.assertFalse(active_batches.filter(lot_no='3').exists())

    def test_active_does_not_return_expired_batches(self):
        Batch.objects.create(lot_no='1', is_active=True, valid_from=self.last_week, expires=self.yesterday)
        active_batches = Batch.objects.active()
        self.assertFalse(active_batches.exists())


class BatchTestCase(TestCase):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)
    last_week = today - datetime.timedelta(days=7)

    def test_is_active_when_is_active_is_set(self):
        batch = Batch(is_active=True, valid_from=self.last_week, expires=self.tomorrow)
        self.assertEqual(batch.status, 'active')

    def test_is_inactive_when_is_active_is_set_but_batch_expired(self):
        batch = Batch(is_active=True, valid_from=self.last_week, expires=self.yesterday)
        self.assertEqual(batch.status, 'inactive')

    def test_is_inactive_when_is_active_is_not_set(self):
        batch = Batch(is_active=False, valid_from=self.last_week, expires=self.tomorrow)
        self.assertEqual(batch.status, 'inactive')

    def test_display_as_inactive_when_inactive_and_date_is_valid(self):
        with freeze_time("2001-02-01 06:00:00"):
            batch = Batch(is_active=False, valid_from=datetime.date(2001, 1, 1), expires=datetime.date(2001, 3, 1))
            self.assertFalse(batch.display_as_active)
            self.assertIsInstance(batch.display_as_active, bool)

    def test_display_as_inactive_when_inactive_and_not_yet_valid(self):
        with freeze_time("2001-02-01 06:00:00"):
            batch = Batch(is_active=False, valid_from='2001-02-10', expires=datetime.date(2001, 3, 1))
            self.assertFalse(batch.display_as_active)
            self.assertIsInstance(batch.display_as_active, bool)

    def test_display_as_inactive_when_inactive_and_expired(self):
        with freeze_time("2001-02-01 06:00:00"):
            batch = Batch(is_active=False, valid_from=datetime.date(2001, 1, 1), expires='2001-01-10')
            self.assertFalse(batch.display_as_active)
            self.assertIsInstance(batch.display_as_active, bool)

    def test_display_as_inactive_when_active_and_not_yet_valid(self):
        with freeze_time("2001-02-01 06:00:00"):
            batch = Batch(is_active=True, valid_from=datetime.date(2001, 2, 10), expires=datetime.date(2001, 3, 1))
            self.assertFalse(batch.display_as_active)
            self.assertIsInstance(batch.display_as_active, bool)

    def test_display_as_inactive_when_active_and_expired(self):
        with freeze_time("2001-02-01 06:00:00"):
            batch = Batch(is_active=True, valid_from=datetime.date(2001, 1, 1), expires=datetime.date(2001, 1, 10))
            self.assertFalse(batch.display_as_active)
            self.assertIsInstance(batch.display_as_active, bool)

    def test_display_as_active_when_active_and_valid(self):
        with freeze_time("2001-02-01 06:00:00"):
            batch = Batch(is_active=True, valid_from=datetime.date(2001, 1, 1), expires=datetime.date(2001, 3, 1))
            self.assertTrue(batch.display_as_active)
            self.assertIsInstance(batch.display_as_active, bool)
        with freeze_time("2001-01-01 00:00:00"):
            batch = Batch(is_active=True, valid_from=datetime.date(2001, 1, 1), expires=datetime.date(2001, 3, 1))
            self.assertTrue(batch.display_as_active)
            self.assertIsInstance(batch.display_as_active, bool)
        with freeze_time("2001-03-01 23:59:59"):
            batch = Batch(is_active=True, valid_from=datetime.date(2001, 1, 1), expires=datetime.date(2001, 3, 1))
            self.assertTrue(batch.display_as_active)
            self.assertIsInstance(batch.display_as_active, bool)

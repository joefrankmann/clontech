from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse


class Feedback(models.Model):
    rating_choices = [
        ("good", "good"),
        ("okay", "okay"),
        ("poor", "poor")
    ]
    uploader_email = models.EmailField(
        _("Uploader Email"), blank=False, null=False)
    created_at = models.DateTimeField(
        _("Created At"), blank=False, null=False, auto_now=True)
    device_os = models.CharField(
        _("Device OS"), max_length=255, blank=True, null=False, default="",
        help_text=_('operating system of the device'))
    device_make = models.CharField(
        _("Device Make"), max_length=255, blank=True, null=False, default="",
        help_text=_('manufacturer/brand of the device'))
    device_model = models.CharField(
        _("Device Model"), max_length=255, blank=True, null=False, default="")
    device_id = models.CharField(
        _("Device ID"), max_length=255, blank=True, null=False, default="")
    app_version = models.CharField(
        _("App version"), max_length=255, blank=True, null=False, default="")
    reader_type = models.CharField(
        _("Reader type"), max_length=255, blank=True, null=False, default="")
    reader_version = models.CharField(
        _("Reader version"), max_length=255, blank=True, null=False, default="")
    rating = models.CharField(
        _("Rating"), max_length=255, blank=False, null=False, choices=rating_choices)
    follow_up = models.BooleanField(_("Follow up"), null=False, blank=False, help_text=_(
        "Receive a follow up on this feedback from one of our team?"))
    comments = models.TextField(
        _("Comments"), null=False, blank=False, default="", help_text=_("General comments on the app and product"))

    csv_fields = [
        ('created_at', 'created_at'),
        ('id', 'pk'),
        ('uploader_email', 'uploader_email'),
        ('device', 'device'),
        ('reader', 'reader'),
        ('app_version', 'app_version'),
        ('device_id', 'device_id'),
        ('rating', 'rating'),
        ('follow_up', 'follow_up_str'),
        ('comments', 'comments')
    ]

    @property
    def device(self) -> str:
        return " ".join([self.device_os, self.device_make, self.device_model])

    @property
    def reader(self) -> str:
        return " ".join([self.reader_type, self.reader_version])

    def get_absolute_url(self) -> str:
        return reverse("ndx_feedback:feedback-detail", kwargs={"pk": self.pk})

    @classmethod
    def get_csv_headers(cls) -> [str]:
        return [field[0] for field in cls.csv_fields] 

    @property
    def csv_row(self) -> [str]:
        return [str(getattr(self, field[1])) for field in self.csv_fields]

    @property
    def follow_up_str(self) -> [str]:
        if self.follow_up:
            return 'yes'
        return 'no'

    class Meta:
        permissions = [
            ("view_feedback", _("Can view feedback")),
        ]
        ordering = ["-created_at"]

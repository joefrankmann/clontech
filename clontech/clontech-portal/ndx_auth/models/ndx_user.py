from ndx_auth_source.models.ndx_user import *  # noqa
import ndx_auth_source.models.ndx_user as source  # noqa

from django.db import models
from django.utils.translation import ugettext_lazy as _


class NdxUser(source.NdxUser):
    feedback_emails = models.BooleanField(_("Receives feedback emails"), blank=True, default=False, help_text=_(
        "Indicates whether this user should receive emails notifying them feedback has been submitted."))

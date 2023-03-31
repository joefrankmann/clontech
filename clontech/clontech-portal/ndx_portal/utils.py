"""General utility functions."""

from ndx_auth.models import NdxUser


def qc_user_emails():
    emails = []
    for user in NdxUser.objects.all():
        if user.user_type == "QC User":
            emails.append(user.email)
    return emails

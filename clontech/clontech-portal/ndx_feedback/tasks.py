import celery
import logging

from django.conf import settings
from django.core.mail import send_mail
from smtplib import SMTPException

logger = logging.getLogger(__name__)


@celery.shared_task(bind=True)
def send_feedback_email(self, rendered_template, user_email):
    """
    Celery task to send a feedback email to an individual user, with a preformatted template.
    """
    try:
        logger.debug('Attempting to send feedback email to {}'.format(user_email))
        send_mail(
            "{} feedback".format(settings.SITE_NAME),
            rendered_template,
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False
        )
        logger.debug('Successfully sent feedback email to {}'.format(user_email))

    except SMTPException:
        logger.exception('Failed to send email to {}'.format(user_email))

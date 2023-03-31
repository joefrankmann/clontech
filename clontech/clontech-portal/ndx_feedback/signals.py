from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import loader
from django.conf import settings


from ndx_feedback.models import Feedback
from ndx_feedback.tasks import send_feedback_email
from ndx_auth.models import NdxUser


@receiver(post_save, sender=Feedback, dispatch_uid="ndx_feedback_save")
def send_feedback_notification_emails(sender, instance, created, **kwargs):
    """
    Receiver function that will send notification emails after a new feedback has been submitted.
    """
    if created:
        context = {
            "feedback": instance,
            "site_name": settings.SITE_NAME
        }
        # The template is not receiver specific so can be rendered once before sending
        template = loader.get_template('ndx_feedback/notification_email.txt')
        rendered_template = template.render(context)
        for user in NdxUser.objects.filter(feedback_emails=True):
            send_feedback_email.delay(rendered_template, user.email)

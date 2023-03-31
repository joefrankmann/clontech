from ndx_auth_source.forms.ndx_user import *  # noqa
import ndx_auth_source.forms.ndx_user as source  # noqa

from django import forms
from django.core.exceptions import ValidationError
from ndx_auth.models import NdxUser, UserType


feedback_emails_field = forms.BooleanField(required=False, label="User receives feedback emails")
user_type_field = forms.ChoiceField(
    required=True,
    label="Group",
    choices=[],
)


class FormValidationMixin():

    def clean(self):
        """
        QC Users are not allowed to receive emails notifying them of feedback and as such this form should
        throw an error if this is set to happen. The form still needs to have both options though in case
        the user type is changed.
        """
        cleaned_data = super().clean()
        feedback_emails = cleaned_data.get("feedback_emails")
        user_type = cleaned_data.get("user_type")
        if feedback_emails and user_type == "qc user":
            raise ValidationError("QC Users cannot receive feedback emails.")


class UserForm(FormValidationMixin, source.UserForm):
    """
    Differs in that we have a feedback_emails_field and set the user_type.
    """
    feedback_emails = feedback_emails_field
    user_type = user_type_field

    class Meta:
        model = NdxUser
        fields = ('email', 'name', 'user_type', 'feedback_emails')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        user_type_field = self.fields['user_type']
        user_type_field.choices = self._user_type_choices()

    def save(self, *args, **kwargs) -> NdxUser:
        user = super().save(*args, **kwargs)
        user.feedback_emails = self.cleaned_data['feedback_emails']
        user.update_user_type(UserType.get(self.cleaned_data['user_type']))
        user.save()
        return user


class UserUpdateForm(FormValidationMixin, source.UserUpdateForm):

    feedback_emails = feedback_emails_field
    user_type = user_type_field

    class Meta:
        model = NdxUser
        fields = ('email', 'name', 'user_type', 'feedback_emails')

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        feedback_emails = self.fields['feedback_emails']
        feedback_emails.initial = NdxUser.objects.get(pk=self.instance.pk).feedback_emails

    def save(self, *args, **kwargs) -> NdxUser:
        user = super().save(*args, **kwargs)
        user.update_user_type(UserType.get(self.cleaned_data['user_type']))
        user.feedback_emails = self.cleaned_data['feedback_emails']
        user.save()
        return user

from django.db import transaction
from django.forms import ModelForm, DateTimeInput, HiddenInput, ClearableFileInput
from ndx_audit_log.utils import log_request
from ndx_django_utils.forms.mixins import RequestMixin
from rest_framework.renderers import JSONRenderer

from .models import Eula, EulaFile
from .serializers import EulaSerializer


def render_eula_to_json(eula: Eula) -> bytes:
    return JSONRenderer().render(EulaSerializer(instance=eula).data)


class EulaEditLogMixin(RequestMixin):
    def save(self, commit=True, *args, **kwargs):
        if commit:
            if self._is_new_object:
                old_eula_data = None
            else:
                old_eula_data = render_eula_to_json(self.Meta.model.objects.get(pk=self.instance.pk))
        with transaction.atomic():
            eula = super().save(*args, **kwargs)
            if commit:
                if self._is_new_object:
                    log_request(self._request, "create eula {}".format(eula.pk))
                else:
                    log_request(self._request, "edit eula {}".format(eula.pk), json_attachment=old_eula_data)
        return eula


class FormattedDateTimeInput(DateTimeInput):
    input_type = 'datetime-local'

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M:%S"
        super().__init__(**kwargs)


class EulaForm(EulaEditLogMixin, ModelForm):
    class Meta:
        fields = ('is_active', 'valid_from')
        model = Eula
        error_messages = {
            'valid_from': {
                'invalid': ("Enter a valid date/time with format YYYY-MM-DDTHH:MM:SS."),
            },
        }

    def __init__(self, is_create_view, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = kwargs['request']
        self._is_new_object = is_create_view
        self.fields["valid_from"].widget = FormattedDateTimeInput()
        self.fields["valid_from"].input_formats = ["%Y-%m-%dT%H:%M:%S"]


class EulaFileInput(ClearableFileInput):
    template_name = 'ndx_eula/eulafile_input_widget.html'
    

class EulaFileForm(ModelForm):
    class Meta:
        fields = ('eula', 'locale', 'eula_file')
        model = EulaFile

    def __init__(self, request, eula, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._request = request
        self.eula_id = eula
        self.fields['eula'].initial = eula
        self.fields['eula'].widget = HiddenInput()
        self.fields['eula'].disabled = True
        self.fields['eula_file'].required = True
        self.fields['eula_file'].widget = EulaFileInput()

    def save(self, commit=True, *args, **kwargs):
        with transaction.atomic():
            eula_file = super().save(*args, **kwargs)
            log_request(self._request, "edit eula {}".format(eula_file.eula.id))
        return eula_file

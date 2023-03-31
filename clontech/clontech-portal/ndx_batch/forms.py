import django.forms
from django.utils.translation import ugettext_lazy as _
from extra_views import InlineFormSet

from .models import Batch, QuadraticCurveParameters


class QuadraticCurveParametersInlineFormSet(InlineFormSet):
    model = QuadraticCurveParameters
    exclude = ()
    factory_kwargs = {'can_delete': False, 'extra': 1, 'min_num': 1}


class DateInput(django.forms.TextInput):
    """
    Datefields are rendered as "text" inputs by the forms template tag. 
    This form class will override TextInputs to give them Date field functionality 
    """
    input_type = 'date'


class BatchForm(django.forms.ModelForm):
    _is_new_object = True
    
    class Meta:
        model = Batch
        fields = ('lot_no', 'assay_type', 'unit', 'valid_from', 'expires', 'is_active', 'comments')
        widgets = {
            'valid_from': DateInput(),
            'expires': DateInput(),
        }

    def clean(self) -> dict:
        data = super().clean()
        valid_from = data.get('valid_from')
        expires = data.get('expires')
        if valid_from and expires and valid_from >= expires:
            self.add_error('expires', _("Expiry must be after manufacture date."))
        return data


class BatchUpdateForm(BatchForm):
    _is_new_object = False

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['lot_no'].disabled = True

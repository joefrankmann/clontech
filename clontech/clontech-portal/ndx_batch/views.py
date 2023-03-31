from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.urls import reverse
from django.utils.translation import ugettext_lazy
from django.views.generic import ListView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from rest_framework.renderers import JSONRenderer

from ndx_audit_log.utils import log_request
from ndx_django_utils.views.mixins import BreadcrumbMixin, PageTitleMixin

from .forms import BatchForm, BatchUpdateForm, QuadraticCurveParametersInlineFormSet
from .models import Batch
from .serializers import BatchSerializer


def render_batch_to_json(batch: Batch) -> bytes:
    return JSONRenderer().render(BatchSerializer(instance=batch).data)


class BatchListView(BreadcrumbMixin, PermissionRequiredMixin, PageTitleMixin, ListView):
    model = Batch
    page_title = ugettext_lazy("Batches")
    context_object_name = 'batches'
    permission_required = 'ndx_batch.change_batch'
    breadcrumbs = (('ndx_batch:batches', 'Batches'), )


class BatchViewMixin(BreadcrumbMixin, PermissionRequiredMixin, PageTitleMixin):
    model = Batch
    inlines = (QuadraticCurveParametersInlineFormSet,)
    context_object_name = 'batch'

    breadcrumbs = (('ndx_batch:batches', 'Batches'), )

    def get_success_url(self):
        return reverse('ndx_batch:batches')


class BatchView(BatchViewMixin, UpdateWithInlinesView):
    page_title = ugettext_lazy("Manage Batch")
    permission_required = 'ndx_batch.change_batch'
    form_class = BatchUpdateForm

    def get_success_url(self):
        return super().get_success_url()

    def forms_valid(self, form, inlines):
        with transaction.atomic():
            batch = form.instance
            old_batch_data = render_batch_to_json(batch)
            response = super().forms_valid(form, inlines)
            log_request(self.request, "edit batch {}".format(batch.lot_no), json_attachment=old_batch_data)
        return response


class BatchCreateView(BatchViewMixin, CreateWithInlinesView):
    page_title = ugettext_lazy("Create Batch")
    permission_required = 'ndx_batch.add_batch'
    form_class = BatchForm

    def get_success_url(self):
        return super().get_success_url()

    def forms_valid(self, form, inlines):
        with transaction.atomic():
            response = super().forms_valid(form, inlines)
            batch = form.instance
            log_request(self.request, "create batch {}".format(batch.lot_no))
        return response

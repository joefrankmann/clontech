from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


from ndx_audit_log.utils import log_request
from ndx_django_utils.views.mixins import BreadcrumbMixin, RequestMixin
from ndx_eula.forms import EulaForm, EulaFileForm
from ndx_eula.models import Eula, EulaFile


class CommonMixin(BreadcrumbMixin, RequestMixin, PermissionRequiredMixin):
    permission_required = 'ndx_eula.change_eula'
    breadcrumbs = (('ndx_eula:eulas', 'All EULAs'), )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, 'page_title'):
            title = self.page_title
        else:
            title = self.get_page_title()
        context.setdefault('page_title', title)
        return context


class EulaMixin(CommonMixin):
    """Mixin for Eulas"""
    context_object_name = 'eula'
    form_class = EulaForm
    model = Eula

    def get_success_url(self):
        return reverse('ndx_eula:eula-detail', args=(self.object.id,))


class EulaFileMixin(CommonMixin):
    """Mixin for Eula Files"""
    context_object_name = 'eula_file'
    form_class = EulaFileForm
    model = EulaFile

    def dispatch(self, request, *args, **kwargs):
        """
        Get the Eula id from kwargs which will either include 'eula' or 'pk'
        """
        try:
            self.eula_id = self.kwargs['eula']
        except KeyError:
            self.eula_id = EulaFile.objects.get(id=self.kwargs['pk']).eula.id
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('ndx_eula:eula-detail', args=(self.eula_id,))

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['eula'] = self.eula_id
        return form_kwargs

    def get_breadcrumbs(self):
        return (
            ('ndx_eula:eulas', 'All EULAs'), 
            ('ndx_eula:eula-detail', 'EULA {}'.format(self.eula_id), {'pk': self.eula_id})
        )


class EulaListView(EulaMixin, ListView):
    page_title = ugettext_lazy("EULAs")
    context_object_name = 'eulas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            current_eula = Eula.objects.active().past().latest()
        except Eula.DoesNotExist:
            current_eula = None
        context.setdefault('current_eula', current_eula)
        return context


class EulaCreateView(EulaMixin, CreateView):
    page_title = ugettext_lazy("Create EULA")

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['is_create_view'] = True
        return form_kwargs


class EulaDetailView(EulaMixin, DetailView):
    def get_page_title(self):
        return "EULA {}".format(self.object.id)


class EulaUpdateView(EulaMixin, UpdateView):
    def get_page_title(self):
        return "Update EULA {}".format(self.object.id)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['is_create_view'] = False
        return form_kwargs


class EulaAddLanguageView(EulaFileMixin, CreateView):
    def get_page_title(self):
        return "EULA {} - Add language".format(self.eula_id)


class EulaFileUpdateView(EulaFileMixin, UpdateView):
    def get_page_title(self):
        return "Edit EULA entry {}".format(self.object.locale)


class EulaFileDeleteView(EulaFileMixin, DeleteView):
    def get_page_title(self):
        return "Delete EULA entry {}".format(self.object.locale)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        with transaction.atomic():
            success_url = self.get_success_url()
            self.object.delete()
            log_request(request, "edit eula {}".format(self.object.eula.id))
        return HttpResponseRedirect(success_url)

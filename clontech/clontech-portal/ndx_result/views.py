from ndx_result_source.views import *  # noqa
import ndx_result_source.views as source  # noqa

from logging import getLogger
from typing import Dict, Iterable, Sequence

from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db import models
from django.http import (HttpRequest, HttpResponse, HttpResponseForbidden,
                         JsonResponse)
from django.urls import reverse, reverse_lazy
from django.utils.html import conditional_escape, format_html
from django.utils.timezone import localtime
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy
from django.views.generic import TemplateView
from ndx_django_utils.views.mixins import PageTitleMixin

from . import tasks

from ndx_portal.utils import qc_user_emails
from ndx_result.models import Result
from ndx_batch.models import Batch

User = get_user_model()
logger = getLogger(__name__)


class ResultListMixin():
    """
    Simply provide get_queryset to the result view and its ajax counterpart.
    """

    def get_queryset(self) -> models.QuerySet:
        # We need the whole set for this view, because we want to know the total number of records
        queryset = self.model.objects.all()
        user = self.request.user
        if user.has_perm('ndx_result.view_all_results'):
            return queryset
        if user.has_perm('ndx_result.view_qc_results'):
            return queryset.filter(uploader_email__in=qc_user_emails())
        return queryset.none()


class ResultListView(ResultListMixin, source.ResultListView):
    """
    The Results list page served with template. It uses AjaxResultListDataSourceView
    for the data.
    """
    template_name = None  # To override and activate default


class AjaxResultListDataSourceView(ResultListMixin, source.AjaxResultListDataSourceView):
    """
    Provides the data for ResultListView. Gets called whenever filters change etc...
    """
    searchable_columns = ('uploader_email', 'assay_type', 'sample_name', 'device_make')

    def get(self, request, *args, **kwargs) -> HttpResponse:
        try:
            draw = int(request.GET['draw'])
        except KeyError:
            return self._error("draw: missing parameter")
        except ValueError:
            return self._error("draw: not an integer")
        if request.GET.get('search[regex]' != 'false'):
            return self._error("regex search not implemented")
        search_value = request.GET.get('search[value]', '')
        try:
            order_column = int(request.GET.get('order[0][column]', 0))
        except ValueError:
            logger.exception("Exception caught parsing order[0][column]")
            return self._error("order[0][column]: not an integer")
        order_dir = request.GET.get('order[0][dir]', 'asc')
        if order_dir not in ('asc', 'desc'):
            return self._error("order[0][dir]: not asc or decs")
        try:
            start = int(request.GET.get('start', 0))
        except ValueError:
            logger.exception("Exception caught parsing start")
            return self._error("start: not an integer")
        try:
            length = int(request.GET.get('length', 25))
        except ValueError:
            logger.exception("Exception caught parsing length")
            return self._error("length: not an integer")
        try:
            columns = self._parse_columns()
        except (KeyError, ValueError):
            logger.exception("Exception caught parsing columns")
            return self._error("columns: parse error")

        queryset = self.get_queryset()
        num_total_results = queryset.count()
        queryset = self._apply_filters(queryset, columns)
        queryset = self._apply_search(queryset, search_value)
        num_filtered_results = queryset.count()
        distinct_uploader_email = sorted(queryset.order_by().values_list('uploader_email').distinct())
        distinct_assay_type = sorted(queryset.order_by().values_list('assay_type').distinct())
        distinct_sample_name = sorted(queryset.order_by().values_list('sample_name').distinct())
        distinct_device_make = sorted(queryset.order_by().values_list('device_make').distinct())
        queryset = self._apply_ordering(queryset, columns, order_column, order_dir)
        paginator = Paginator(queryset, length)
        data = []
        for result in paginator.page(start / length + 1):
            data.append({
                'created_at': format_html('<a href="{}" target="_blank">{}</a>', result.get_absolute_url(),
                                          localtime(result.created_at).strftime('%c')),
                'uploader_email': format_html(result.uploader_email),
                'assay_type': conditional_escape(result.assay_type),
                'sample_name': format_html(result.sample_name),
                'device_make': format_html("{}", result.device_make),
                'interpretation': format_html("<div class='classification {}'>{}</div>",
                                              result.interpretation.lower(),
                                              result.overall_outcome),
                'action': format_html('<a class="detail" href="{}" target="_blank">'
                                      '<span class="material-icons" aria-hidden="true">forward</span>'
                                      '<span class="sr-only">go to detail view</span></a>',
                                      result.get_absolute_url()),
            })

        return JsonResponse({
            'draw': draw,
            'recordsTotal': num_total_results,
            'recordsFiltered': num_filtered_results,
            'data': data,
            'distinct_column_values': {
                'uploader_email': [x[0] for x in distinct_uploader_email],
                'assay_type': [x[0] for x in distinct_assay_type],
                'sample_name': [x[0] for x in distinct_sample_name],
                'device_make': [" ".join(device) for device in distinct_device_make],
            },
        })

    @staticmethod
    def _apply_filters(
            queryset: models.QuerySet,
            columns: Iterable[Dict[str, str]]) -> models.QuerySet:
        filters = models.Q()
        for column in columns:
            search_value = column['search_value']
            if search_value:
                filter_name = column['data']
                if filter_name == 'sample_name':
                    filters &= models.Q(**{filter_name: search_value})
                if filter_name == 'assay_type':
                    filters &= models.Q(**{filter_name: search_value})
                if filter_name == 'device_make':
                    filters &= models.Q(**{filter_name: search_value})
                elif filter_name == 'uploader_email':
                    filters &= models.Q(uploader_email=search_value)
        if filters:
            return queryset.filter(filters)
        return queryset

    @staticmethod
    def _apply_ordering(
            queryset: models.QuerySet,
            columns: Sequence[Dict[str, str]],
            order_column: int,
            order_dir: str) -> models.QuerySet:
        column_name = columns[order_column]['name']
        # The columns which can be used for ordering. We need to refactor this in shadow apps to make it better
        if column_name not in ('created_at', 'uploader_email', 'assay_type', 'sample_name', 'device_make'): 
            return queryset
        if order_dir == 'desc':
            column_name = '-{}'.format(column_name)
        return queryset.order_by(column_name)


class ResultListCsvView(source.ResultListCsvView):

    def post(self, request: HttpRequest) -> HttpResponse:
        user = request.user
        # permissions differ from source
        if not (user.has_perm('ndx_result.view_all_results') or user.has_perm('ndx_result.view_qc_results')):
            return HttpResponseForbidden()

        async_result = tasks.export_results_to_csv_file.delay(user_id=user.pk)
        task_id = self._get_task_id(async_result)

        return JsonResponse(
            {
                'status': "pending",
                'status_url': "{}?{}".format(reverse('ndx_result:results-csv'), urlencode({'task_id': task_id})),
            }
        )


class ResultView(source.ResultView):

    queryset = Result.objects.select_related('batch', 'geo_location').prefetch_related('teststrips')

    def get_object(self, queryset: models.QuerySet = None) -> Result:
        result = super().get_object(queryset=queryset)
        user = self.request.user
        if user.has_perm('ndx_result.view_all_results'):
            return result
        if user.has_perm('ndx_result.view_qc_results'):
            if result.uploader_email in qc_user_emails():
                return result
        raise PermissionDenied()


class ResultPrintView(source.ResultPrintView):
    page_title = ugettext_lazy("Clontech Result")


class ResultCsvDownloadView(PermissionRequiredMixin, PageTitleMixin, TemplateView):
    page_title = ugettext_lazy("Results CSV Download")
    context_object_name = 'result'
    template_name = "ndx_result/result_csv_download.html"
    fields = ['date range', 'assay_type', 'lot_number']  
    success_url = reverse_lazy('ndx_result:results')
    permission_required = 'ndx_result.view_result'
    model = Result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assay_types = [a[0] for a in sorted(Result.objects.all().order_by().values_list('assay_type').distinct())]
        context['assay_types'] = assay_types
        context['lot_nos'] = sorted(batch.lot_no for batch in Batch.objects.all())
        context['assay_types'].insert(0, settings.NDX_SELECT_ALL)
        context['lot_nos'].insert(0, settings.NDX_SELECT_ALL)
        return context

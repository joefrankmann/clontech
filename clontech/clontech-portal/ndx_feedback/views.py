from ndx_feedback.models import Feedback
from django.db import models
from django.http import JsonResponse
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.translation import ugettext_lazy
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.html import format_html
from ndx_django_utils.views.mixins import BreadcrumbMixin, PageTitleMixin
from django.core.paginator import Paginator
from logging import getLogger
from typing import List, Dict, Sequence  # noqa
from itertools import count

logger = getLogger(__name__)


class FeedbackMixin(BreadcrumbMixin, PermissionRequiredMixin, PageTitleMixin):
    model = Feedback
    breadcrumbs = (('ndx_feedback:feedback', 'Feedback'), )
    permission_required = 'ndx_feedback.view_feedback'
    context_object_name = 'feedback'


class FeedbackListView(FeedbackMixin, TemplateView):
    page_title = ugettext_lazy('Feedback')
    template_name = "ndx_feedback/feedback_list.html"


class FeedbackDetailView(FeedbackMixin, DetailView):
    page_title = ugettext_lazy('Feedback Detail')
    template_name = 'ndx_feedback/feedback_detail.html'


# TODO Move to AjaxListView Mixin
class FeedbackAjaxListView(ListView, PermissionRequiredMixin):
    permission_required = 'ndx_feedback.view_feedback'

    def get_queryset(self):
        return Feedback.objects.all()

    def get(self, request, *args, **kwargs):
        columns = self.get_columns()
        queryset = self._get_queryset_with_parameters(columns)
        paginator = Paginator(queryset, self.get_length())

        return JsonResponse({
            'draw': self.get_draw(),
            'recordsTotal': Feedback.objects.count(),
            'recordsFiltered': queryset.count(),
            'data': self.get_data(paginator),
            'distinct_column_values': self.get_distinct_column_values(queryset)
        })

    def get_data(self, paginator):
        data = []
        created_at_html = """
        <td data-sort={}>
            <a href="{}">
              {}
            </a>
          </td>
        """
        action_html = """
        <td>
            <a href="{}" class="detail">
              <span class="material-icons" aria-hidden="true">forward</span>
              <span class="sr-only">link to feedback detail</span>
            </a>
          </td>
        """
        for entry in paginator.page(self.get_start() / self.get_length() + 1):
            result_dict = {
                'created_at': format_html(
                    created_at_html, 
                    entry.created_at.isoformat(), 
                    entry.get_absolute_url(), 
                    entry.created_at.strftime("%d %B %Y, %H:%M:%S")),
                'uploader_email': format_html("<td>{}</td>", entry.uploader_email),
                'rating': format_html("<td>{}</td>", entry.rating),
                'device_id': format_html("<td>{}</td>", entry.device_id),
                'follow_up': format_html("<td>{}</td>", entry.follow_up_str),
                'action': format_html(action_html, entry.get_absolute_url())
            }
            data.append(result_dict)
        return data

    def get_distinct_column_values(self, queryset):
        distinct_created_at = queryset.order_by().values_list('created_at').distinct()
        distinct_uploader_email = queryset.order_by().values_list('uploader_email').distinct()
        distinct_rating = queryset.order_by().values_list('rating').distinct()
        distinct_device_id = queryset.order_by().values_list('device_id').distinct()
        distinct_follow_up = queryset.order_by().values_list('follow_up').distinct()

        def convert(val):
            if val:
                return 'yes'
            return 'no'

        return {
            'created_at': [x[0] for x in distinct_created_at],
            'uploader_email': [x[0] for x in distinct_uploader_email],
            'rating': [x[0] for x in distinct_rating],
            'device_id': [x[0] for x in distinct_device_id],
            'follow_up': [convert(i[0]) for i in distinct_follow_up],
            'action': []
        }

    def _parse_columns(self) -> List[Dict[str, str]]:
        columns = []  # type: List[Dict[str, str]]
        for col_index in count(0):
            def coldata(key):
                return self.request.GET['columns[{}]{}'.format(col_index, key)]
            try:
                data = self.request.GET['columns[{}][data]'.format(col_index)]
            except KeyError:
                return columns
            if coldata('[search][regex]') == 'true':
                raise ValueError("regex search not implemented")
            columns.append({
                'data': data,
                'name': coldata('[name]'),
                'orderable': coldata('[orderable]'),
                'searchable': coldata('[searchable]'),
                'search_value': coldata('[search][value]'),
            })

    def _get_filters(self, columns):
        filters = models.Q()
        for column in columns:
            try:
                filter_value = column["search_value"]
                filter_key = column["data"]
            except KeyError:
                continue
            if filter_value != "":
                # Convert yes/no into boolean for follow_up column
                if column['name'] == 'follow_up':
                    filter_value = filter_value.lower() == 'yes'
                filters &= models.Q(**{filter_key: filter_value})
        return filters

    def _get_search_term(self):
        if self.request.GET.get('search[regex]' != 'false'):
            return self._error("regex search not implemented")
        return self.request.GET.get('search[value]', '').strip(' ')

    def _get_search_filters(self, search_term):
        search_filters = models.Q()
        columns = ["uploader_email", "rating", "device_id"]
        for column in columns:
            key = "{}__icontains".format(column)
            search_filters |= models.Q(**{key: search_term})
        return search_filters

    def _apply_ordering(self, columns, queryset):
        order_column_id = self.get_order_column()
        if order_column_id < len(columns):
            order_column = columns[order_column_id]['name']
            ordering = self.get_order_dir()
            ordering_sign = ""
            if ordering == "desc":
                ordering_sign = "-"
            order_arg = "{}{}".format(ordering_sign, order_column)
            return queryset.order_by(order_arg)
        else:
            return queryset

    def _get_queryset_with_parameters(self, columns):
        filters = models.Q()
        filters &= self._get_filters(columns)
        search_term = self._get_search_term()
        if search_term != "":
            filters &= self._get_search_filters(search_term)
        queryset = Feedback.objects.filter(filters)
        queryset = self._apply_ordering(columns, queryset)
        return queryset

    def get_columns(self):
        try:
            return self._parse_columns()
        except (KeyError, ValueError):
            logger.exception("Exception caught parsing columns")
            return self._error("columns: parse error")

    def get_order_column(self):
        try:
            return int(self.request.GET.get('order[0][column]', 0))
        except ValueError:
            logger.exception("Exception caught parsing order[0][column]")
            return self._error("order[0][column]: not an integer")

    def get_order_dir(self):
        order_dir = self.request.GET.get('order[0][dir]', 'asc')
        if order_dir not in ('asc', 'desc'):
            return self._error("order[0][dir]: not asc or decs")
        return order_dir

    def get_draw(self):
        try:
            return int(self.request.GET['draw'])
        except KeyError:
            return self._error("draw: missing parameter")
        except ValueError:
            return self._error("draw: not an integer")

    def get_length(self):
        try:
            return int(self.request.GET.get('length', 25))
        except ValueError:
            logger.exception("Exception caught parsing length")
            return self._error("length: not an integer")

    def get_start(self):
        try:
            return int(self.request.GET.get('start', 0))
        except ValueError:
            logger.exception("Exception caught parsing start")
            return self._error("start: not an integer")


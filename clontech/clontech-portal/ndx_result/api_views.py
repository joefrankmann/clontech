from ndx_result_source.api_views import *  # noqa
import ndx_result_source.api_views as source  # noqa

import csv
from datetime import datetime, timedelta
from typing import Dict
from rest_framework.decorators import api_view
from django.conf import settings
from django.http import HttpRequest, StreamingHttpResponse
from django.utils import timezone

from ndx_result.models import Result
from ndx_portal.utils import qc_user_emails


class FakedBuffer:
    """
    Using a faked buffer which just returns values written into it instead of storing them
    allows a streaming HTTP response to be used, allowing us to more easily transfer large CSV files.
    """

    def write(self, value):
        return value


def generate_filters(request: HttpRequest) -> Dict[str, str]:
    # the various django content filters for each field
    filter_types = {
        "start_date": "created_at__gt",
        "end_date": "created_at__lt",
        "assay_type": "assay_type",
        "lot_no": "batch__lot_no"
    }
    filter_kwargs = {}
    for key in filter_types.keys():
        # only add the filter to the kwargs if a value has been specified
        value = request.GET.get(key, None)
        if value not in (None, settings.NDX_SELECT_ALL):
            filter_kwargs[filter_types[key]] = value
    
    # end date needs to be increased by one day to inculde all results before midnight on the user selected end date
    if "created_at__lt" in filter_kwargs:
        end_date = datetime.strptime(filter_kwargs.get("created_at__lt"), "%Y-%m-%d")
        extended_end_date = datetime.strftime(end_date + timedelta(days=1), "%Y-%m-%d")
        filter_kwargs["created_at__lt"] = extended_end_date

    if request.user.has_perm('ndx_result.view_all_results') or request.user.is_superuser:
        return filter_kwargs
    elif request.user.has_perm('ndx_result.view_qc_results'):
        filter_kwargs["uploader_email__in"] = qc_user_emails()
    else:
        filter_kwargs["uploader_email"] = request.user.email

    return filter_kwargs


def csv_generator(queryset, writer, csv_headers, is_qc_user):
    """
    Generator for the streamed CSV file
    """

    # Just some defensive code because of how we're generating headers
    for header in csv_headers:
        assert "," not in header

    # This is the only way which seems to work
    yield ','.join(csv_headers) + '\n'

    for entry in queryset:
        if not entry.has_csv_data:
            entry.save_csv_row()
        row_data = entry.generated_csv_row
        # Remove qc fields
        if is_qc_user:
            for field in Result.fields_to_hide_for_qc:
                del row_data[field]
        yield writer.writerow(row_data)


@api_view(http_method_names=["GET"])
def result_csv_view(request: HttpRequest, *args, **kwargs) -> StreamingHttpResponse:
    filters = generate_filters(request)
    # multiple filters are supplied as django filter kwargs, this gives a large performance 
    # boost compared to filtering the queryset multiple times
    is_qc_user = request.user.user_type == 'QC User'
    csv_headers = [header[0] for header in Result.get_csv_headers()]
    if is_qc_user:
        for field in Result.fields_to_hide_for_qc:
            csv_headers.remove(field)

    faked_buffer = FakedBuffer()
    writer = csv.DictWriter(faked_buffer, fieldnames=csv_headers, extrasaction="ignore")
    generator = csv_generator(Result.objects.filter(**filters), writer, csv_headers, is_qc_user)
    response = StreamingHttpResponse((row for row in generator), content_type="application/csv")
    response['Content-Disposition'] = 'attachment; filename="results_{}.csv"'.format(timezone.now().isoformat())
    return response

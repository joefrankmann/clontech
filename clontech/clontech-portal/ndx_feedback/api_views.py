import json
import csv

from django.http import HttpRequest, StreamingHttpResponse
from django.utils import timezone

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.settings import api_settings

from ndx_audit_log.utils import log_request
from ndx_feedback.models import Feedback
from ndx_feedback.serializers import FeedbackSerializer


class FeedbackViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = (DjangoModelPermissions,)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def create(self, request):
        log_request(request, "new feedback submission", json_attachment=json.dumps(request.data))
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FakedBuffer:
    """
    Using a faked buffer which just returns values written into it instead of storing them
    allows a streaming HTTP response to be used, allowing us to more easily transfer large CSV files.
    """

    def write(self, value):
        return value


@api_view(http_method_names=['GET'])
def feedback_csv_view(request: HttpRequest, *args, **kwargs) -> StreamingHttpResponse:
    """
    endpoint: /api/feedback/csv/
    This endpoint is for the API view to access the feedback CSV download, which is generated and sent
    as a StreamingHttpResponse, this allows for transfers of large CSV files and the specific method
    negates the need for celery to be used. Decreasing the complexity of the frontend code needed and
    reducing celery related errors.
    """
    rows = [Feedback.get_csv_headers()]
    rows.extend([entry.csv_row for entry in Feedback.objects.all()])
    faked_buffer = FakedBuffer()
    writer = csv.writer(faked_buffer)
    response = StreamingHttpResponse((writer.writerow(row) for row in rows), content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="feedback_results_{}.csv"'.format(
        timezone.now().isoformat())
    return response

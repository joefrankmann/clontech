from rest_framework import authentication, generics
from rest_framework.settings import api_settings
import rest_framework

from .models import Batch, BatchQueryset
from .serializers import BatchSerializer
from .pagination import FlexiblePageNumberPagination


class ActiveBatchesView(generics.ListAPIView):
    serializer_class = BatchSerializer
    permission_classes = (rest_framework.permissions.IsAuthenticated,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [authentication.BasicAuthentication]
    pagination_class = FlexiblePageNumberPagination

    def get_queryset(self) -> BatchQueryset:
        return Batch.objects.active()

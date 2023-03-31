from logging import getLogger

from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import authentication, generics
from rest_framework.settings import api_settings
import rest_framework
import rest_framework.serializers

from .models import Eula
from .serializers import EulaSerializer

logger = getLogger()


class LazyStr(object):
    def __init__(self, eager_fun):
        self._fun = eager_fun

    def __str__(self):
        return str(self._fun())


class CurrentEulaView(generics.RetrieveAPIView):
    queryset = Eula.objects.active()
    serializer_class = EulaSerializer
    permission_classes = (rest_framework.permissions.IsAuthenticated,)
    authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES + [authentication.BasicAuthentication]

    _logger = logger.getChild('CurrentEulaView')

    def get_queryset(self):
        return super().get_queryset().past()

    def get_object(self):
        self._logger.debug('get_object: Number of active EULAs: %s', LazyStr(lambda: self.get_queryset().count()))
        eula = self._get_eula_or_not_found()

        last_accepted = self._parse_last_accepted()
        if last_accepted is not None and last_accepted > eula.valid_from:
            raise rest_framework.exceptions.NotFound("Newer Eula does not exist.")

        self._logger.debug('get_object: Valid EULA returned.')
        return eula

    def _get_eula_or_not_found(self):
        queryset = self.get_queryset()
        self._logger.debug(
            '_get_eula_or_not_found: Active EULAs: %s',
            LazyStr(lambda: ', '.join(str(e.pk) for e in queryset)))
        try:
            return queryset[0]
        except IndexError:
            raise rest_framework.exceptions.NotFound("Valid EULA not found.")

    def _parse_last_accepted(self):
        last_accepted = self.request.query_params.get('last_accepted', None)
        if last_accepted is not None:
            try:
                last_accepted_dt = parse_datetime(last_accepted)
            except ValueError:
                raise rest_framework.serializers.ValidationError({
                    'last_accepted': "Must be a valid datetime (ISO8601 with timezone offset)."})
            if last_accepted_dt is not None:
                if timezone.is_naive(last_accepted_dt):
                    raise rest_framework.serializers.ValidationError({
                        'last_accepted': "Missing timezone offset."})
                return last_accepted_dt
        return None

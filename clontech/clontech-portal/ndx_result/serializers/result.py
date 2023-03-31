from ndx_result_source.serializers.result import *  # noqa
import ndx_result_source.serializers.result as source  # noqa

from django.conf import settings
from django.db import transaction
from logging import getLogger
from rest_framework import serializers

from ndx_batch.models import Batch
from ndx_result.models import Result, TLine, Teststrip, ResultGeoLocation

logger = getLogger(__name__)


class ResultSerializer(source.ResultSerializer):
    batch_no = serializers.CharField(max_length=255, required=False)
    interpretations = None
    location = None

    class Meta:
        model = Result
        fields = ('analysis_type', 'app_version', 'assay_type', 'average_iteration_time',
                  'batch', 'batch_no', 'created_at', 'created_by', 'device_id', 'device_make',
                  'device_model', 'device_os', 'dilution', 'first_occurrence_of_green_time',
                  'first_occurrence_of_yellow_time', 'geo_location', 'gostix_value', 'guid',
                  'interpretation', 'is_reference', 'notes', 'reader_type', 'reader_version',
                  'reference_name', 'sample_id', 'sample_name', 'teststrips', 'titre',
                  'transition_to_result_time', 'unit', 'uploader_email'
                  )
        read_only_fields = ('created_by',)
        depth = 4

    def create(self, validated_data):
        try:
            batch = Batch.objects.get(lot_no=validated_data.pop('batch_no', None))
        except Batch.DoesNotExist:
            batch = None
        geo_location_data = validated_data.pop('geo_location', None)
        teststrips_data = validated_data.pop('teststrips')
        result_data = validated_data.copy()
        result_data['batch'] = batch

        # Deal with fields which model allows blank, but we can't make blank=False in the model
        # This is because we need to allow blank uploader_email (Apple being twats) but don't
        # want it blank in the db because it messes with datatable filtering.
        for field in ['uploader_email', 'sample_name']:
            value = validated_data.pop(field, '')
            if str(value).strip() in ('', 'None'):
                result_data[field] = settings.NDX_BLANK_LEGACY_PLACEHOLDER

        if self._unparsed_data is not None:
            result_data['unparsed_data'] = self._unparsed_data
        with transaction.atomic():
            result = Result.objects.create(**result_data)
            for teststrip_data in teststrips_data:
                tlines = [TLine(**tld) for tld in teststrip_data.pop('tlines')]
                teststrip = Teststrip.objects.create(result=result, **teststrip_data)
                teststrip.tlines.add(*tlines, bulk=False)
            if geo_location_data is not None:
                ResultGeoLocation.objects.create(
                    result=result,
                    **geo_location_data)
        return result

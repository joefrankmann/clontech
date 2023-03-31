from ndx_result_source.serializers.result_converters import *  # noqa
import ndx_result_source.serializers.result_converters as source  # noqa

from django.utils.dateparse import parse_datetime, parse_duration
from ndx_result.serializers.convert import RF, MRF, FlattenedResultField


RESULT_CONVERTERS = {
    'DeviceOS': RF('device_os'),
    'DeviceModel': RF('device_model'),
    'IsPending': NotImplemented,
    'ReaderAnalysisType': RF('analysis_type'),
    'AppVersion': RF('app_version'),
    'AssayType': RF('assay_type'),
    'ReaderType': RF('reader_type'),
    'NDXImagingVersion': RF('reader_version'),
    'DeviceID': RF('device_id'),
    'UniqueId': RF('sample_id'),
    'Timestamp': RF('created_at', parse_datetime),
    'Operator': NotImplemented,
    'DeviceMake': RF('device_make'),
    'Email': RF('uploader_email'),
    'Id': RF('guid'),
    'Location': NotImplemented,
    'GeolocationLatitude': RF('geo_location.latitude'),
    'GeolocationLongitude': RF('geo_location.longitude'),
    'Notes': RF('notes'),
    'Interpretations': FlattenedResultField({
        'Classification': RF('interpretation'),
        'Colour': NotImplemented,
    }),
    'Interpretation': NotImplemented,
    'BatchID': RF('batch_no'),
    'ClontechResult': FlattenedResultField({
        'Dilution': RF('dilution'),
        'IFU': NotImplemented,
        'IsRefSample': RF('is_reference'),
        'MOI': NotImplemented,
        'RefName': RF('reference_name'),
        'SampleName': RF('sample_name'),
        'Unit': RF('unit'),
        'Titre': RF('titre'),
        'GV': RF('gostix_value'),
    }),
    'TestStrips': MRF('teststrips', {
        'Profile': RF('profile'),
        'Baseline': RF('baseline'),
        'CLine': FlattenedResultField({
            'CPeakPosition': RF('cline_peak_position'),
            'CScore': RF('cline_score'),
            'RightMaximaValue': NotImplemented,
            'RightMaximaIndex': NotImplemented,
            'LeftMaximaIndex': NotImplemented,
            'LeftMaximaValue': NotImplemented,
            'CPeakUpperBound': NotImplemented,
            'CPeakLowerBound': NotImplemented,
        }),
        'TLines': MRF('tlines', {
            'TPeakPosition': RF('peak_position'),
            'TScore': RF('score'),
            'TCRatio': RF('t_c_ratio'),
            'TCRatioError': NotImplemented,
            'RightMaximaValue': NotImplemented,
            'RightMaximaIndex': NotImplemented,
            'LeftMaximaValue': NotImplemented,
            'LeftMaximaIndex': NotImplemented,
            'TPeakUpperBound': NotImplemented,
            'TPeakLowerBound': NotImplemented,
            'TScoreError': NotImplemented,
        }),
        'StripImageBase64': RF('image'),
    }),
    'TimeStampInfo': FlattenedResultField({
        'AverageIterationTime': RF('average_iteration_time', parse_duration),
        'TransitionToResultTimeStamp': RF('transition_to_result_time', parse_duration),
        'FirstOccuranceOfGreenTimeStamp': RF('first_occurrence_of_green_time', parse_duration),
        'FirstOccuranceOfYellowTimeStamp': RF('first_occurrence_of_yellow_time', parse_duration),
    }),
}

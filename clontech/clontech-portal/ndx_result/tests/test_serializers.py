from ndx_result_source.tests.test_serializers import *  # noqa
import ndx_result_source.tests.test_serializers as source  # noqa

import datetime

from ndx_batch.models import Batch


class ResultSerializerTestCase(source.ResultSerializerTestCase):
    """
    Some tests resemble source app tests, the only difference being Email key,
    and different interpretation format.

    Some tests from source app have been disabled as they are incompatible.
    """
    this_file = __file__

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create()
        cls.batch = Batch.objects.create(
            lot_no="BATCH NUMBER 01",
            expires=datetime.date.today() + datetime.timedelta(days=360),
            valid_from=datetime.date.today() - datetime.timedelta(days=360),
            is_active=True,
        )

    def test_device_display_name_returns_human_readable_device_name_if_it_exists(self):
        pass

    def test_positive_interpretation_is_converted(self):
        pass

    def test_device_display_name_returns_full_device_name(self):
        pass


    def test_base_attributes_are_converted(self):
        mpaf_data = json_load(self.getMpafResultFile())
        mpaf_result = mpaf_data['results'][0]
        serializer = ResultSerializer.from_ndx_result(mpaf_result)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save(created_by=self.user)

        self.assertEqual(result.device_os, mpaf_result['DeviceOS'])
        self.assertEqual(result.device_model, mpaf_result['DeviceModel'])
        self.assertEqual(result.analysis_type, mpaf_result['ReaderAnalysisType'])
        self.assertEqual(result.app_version, mpaf_result['AppVersion'])
        self.assertEqual(result.device_id, mpaf_result['DeviceID'])
        self.assertEqual(result.sample_id, mpaf_result['UniqueId'])
        self.assertEqual(result.created_at, parse_datetime(mpaf_result['Timestamp']))
        self.assertEqual(result.device_make, mpaf_result['DeviceMake'])
        self.assertEqual(result.uploader_email, mpaf_result['Email'])
        self.assertEqual(result.guid, mpaf_result['Id'])

    def test_interpretation_is_converted(self):
        mpaf_data = json_load(self.getMpafResultFile())
        mpaf_result = mpaf_data['results'][0]
        mpaf_interpretation = mpaf_result['Interpretations']
        serializer = ResultSerializer.from_ndx_result(mpaf_result)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save(created_by=self.user)
        interpretation = result.interpretation
        self.assertEqual(interpretation, mpaf_interpretation[0]['Classification'])

    def test_from_mpaf_does_not_alter_result_data(self):
        mpaf_data = {
            "Interpretations": [{"Colour": "#66cc66", "Name": "HRes", "Classification": "Invalid"}],
            "TestStrips": [{
                "Profile": [195.434982, 192.2475, 190.775, 189.0425, 188.695],
                "TLines": [{
                    "TPeakPosition": 3,
                    "TCRatio": 0.29722893238067627,
                    "TScore": 10.74224853515625,
                }],
                "CLine": {
                    "CPeakPosition": 37,
                    "RightMaximaIndex": 0,
                    "CScore": 36.141326904296875
                },
                "Baseline": [221.268021, 221.059326, 220.855453, 220.656418, 220.462189],
                "StripImageBase64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            },
            ],
            "DeviceOS": "10.2",
            "DeviceModel": "iPhone9,3",
            "IsPending": False,
            "GeolocationLatitude": "29.660962664905",
            "AppVersion": "0.2.2.8",
            "Timestamp": "2017-01-20T10:54:21.763199-06:00",
            "ReaderType": "Novarum",
            "DeviceID": "b6d143af-d733-45f3-ad83-1694012d2fc6",
            "UniqueId": '["b6d143af-d733-45f3-ad83-1694012d2fc6","reactor 3","3z","91","3001"]',
            "TimeStampInfo": {
                "AverageIterationTime": "50.364",
                "TransitionToResultTimeStamp": "00:00:09.5801548",
                "FirstOccuranceOfGreenTimeStamp": "00:00:08.7873506"
            },
            "Email": "Test@novarumdx.com",
            "DeviceMake": "Apple",
            "GeolocationLongitude": "-95.5654470585879",
            "Location": "",
        }
        original_mpaf_data = copy.deepcopy(mpaf_data)
        ResultSerializer.from_ndx_result(mpaf_data)
        self.assertDictEqual(mpaf_data, original_mpaf_data)

    def test_additional_data_from_mpaf_is_saved(self):
        mpaf_data = {
            "Interpretations": [{"Colour": "#66cc66", "Name": "HRes", "Classification": "Invalid"}],
            "TestStrips": [{
                "Profile": [195.434982, 192.2475, 190.775, 189.0425, 188.695],
                "TLines": [{
                    "TPeakPosition": 3,
                    "TCRatio": 0.29722893238067627,
                    "TScore": 10.74224853515625,
                }],
                "CLine": {
                    "CPeakPosition": 37,
                    "RightMaximaIndex": 0,
                    "CScore": 36.141326904296875
                },
                "Baseline": [221.268021, 221.059326, 220.855453, 220.656418, 220.462189],
                "StripImageBase64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
            },
            ],
            "DeviceOS": "10.2",
            "DeviceModel": "iPhone9,3",
            "IsPending": False,
            "GeolocationLatitude": "29.660962664905",
            "AppVersion": "0.2.2.8",
            "Timestamp": "2017-01-20T10:54:21.763199-06:00",
            "ReaderType": "Novarum",
            "DeviceID": "b6d143af-d733-45f3-ad83-1694012d2fc6",
            "UniqueId": '["b6d143af-d733-45f3-ad83-1694012d2fc6","reactor 3","3z","91","3001"]',
            "TimeStampInfo": {
                "AverageIterationTime": "50.364",
                "TransitionToResultTimeStamp": "00:00:09.5801548",
                "FirstOccuranceOfGreenTimeStamp": "00:00:08.7873506"
            },
            "DeviceMake": "Apple",
            "GeolocationLongitude": "-95.5654470585879",
            "Location": "",
        }
        serializer = ResultSerializer.from_ndx_result(mpaf_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save(created_by=self.user)
        self.assertTrue(result.unparsed_data)
        unparsed_data = json.loads(result.unparsed_data)
        self.assertEqual(unparsed_data.get('ReaderType', ''), "Novarum")
        self.assertEqual(unparsed_data.get('TestStrips', ({},))[0].get('TLines', ({},))[0].get('TCRatio', 0), 0.29722893238067627)

    def test_clontech_attributes_are_serialized(self):
        result_data = json_load(self.getJsonFile())
        image_data = r'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=='
        for strip in result_data['teststrips']:
            strip['image'] = image_data
        serializer = ResultSerializer(data=result_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save(created_by=self.user)

        self.assertEqual(result.dilution, "1:5")
        self.assertFalse(result.is_reference)
        self.assertEqual(result.reference_name, "TestRef")
        self.assertEqual(result.sample_name, "Sample1")
        self.assertEqual(result.unit, "IFU/ml")
        self.assertAlmostEqual(result.titre, 0.23)
        self.assertEqual(result.notes, "Test")
        self.assertAlmostEqual(result.gostix_value, 809.9532619482943)

    def test_batch_no_is_serialized(self):
        result_data = json_load(self.getJsonFile())
        image_data = r'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=='
        for strip in result_data['teststrips']:
            strip['image'] = image_data
        serializer = ResultSerializer(data=result_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save(created_by=self.user)
        batch = self.batch

        self.assertEqual(result.batch, batch)

    def test_batch_no_is_converted(self):
        mpaf_data = json_load(self.getMpafResultFile())
        mpaf_result = mpaf_data['results'][0]
        serializer = ResultSerializer.from_ndx_result(mpaf_result)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save(created_by=self.user)
        batch = self.batch

        self.assertEqual(result.batch, batch)

    def test_clontech_attributes_are_converted(self):
        mpaf_data = json_load(self.getMpafResultFile())
        mpaf_result = mpaf_data['results'][0]
        serializer = ResultSerializer.from_ndx_result(mpaf_result)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save(created_by=self.user)

        self.assertEqual(result.dilution, "1:5")
        self.assertFalse(result.is_reference)
        self.assertEqual(result.reference_name, "TestRef")
        self.assertEqual(result.sample_name, "Sample1")
        self.assertEqual(result.unit, "IFU/ml")
        self.assertAlmostEqual(result.titre, 0.23)
        self.assertEqual(result.notes, "Test")
        self.assertAlmostEqual(result.gostix_value, 809.9532619482943)

    def test_geo_location_is_converted(self):
        mpaf_data = json_load(self.getMpafResultFile())
        mpaf_result = mpaf_data['results'][0]
        serializer = ResultSerializer.from_ndx_result(mpaf_result)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save(created_by=self.user)

        self.assertTrue(hasattr(result, 'geo_location'))
        self.assertAlmostEqual(result.geo_location.latitude, 29.660962664905)
        self.assertAlmostEqual(result.geo_location.longitude, -95.5654470585879)

    def test_offscale_classification_is_saved(self):
        mpaf_data = json_load(self.getMpafResultFile())
        mpaf_result = mpaf_data['results'][0]
        mpaf_result['Interpretations'][0]['Classification'] = 'OffScale'
        serializer = ResultSerializer.from_ndx_result(mpaf_result)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        result = serializer.save(created_by=self.user)

        self.assertTrue(hasattr(result, 'interpretation'))
        self.assertEqual(result.interpretation, 'OffScale')

# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-15 13:10
from __future__ import unicode_literals

import json

from django.db import migrations, models
import django.db.models.deletion


def forwards(apps, schema_editor):
    Result = apps.get_model('ndx_result', 'Result')  # noqa
    ResultGeoLocation = apps.get_model('ndx_result', 'ResultGeoLocation')  # noqa

    for result in Result.objects.all():
        try:
            unparsed_data = json.loads(result.unparsed_data)
            latitude = unparsed_data.pop('GeolocationLatitude')
            longitude = unparsed_data.pop('GeolocationLongitude')
        except (KeyError, json.decoder.JSONDecodeError):
            continue
        if latitude and longitude:
            ResultGeoLocation.objects.create(result=result, latitude=latitude, longitude=longitude)
            result.unparsed_data = json.dumps(unparsed_data)
            result.save()


def backwards(apps, schema_editor):
    Result = apps.get_model('ndx_result', 'Result')  # noqa
    ResultGeoLocation = apps.get_model('ndx_result', 'ResultGeoLocation')  # noqa

    for location in ResultGeoLocation.objects.all():
        result = location.result
        try:
            unparsed_data = json.loads(result.unparsed_data)
        except json.decoder.JSONDecodeError:
            unparsed_data = {}
        unparsed_data['GeolocationLatitude'] = location.latitude
        unparsed_data['GeolocationLongitude'] = location.longitude
        result.unparsed_data = json.dumps(unparsed_data)
        result.save()
        location.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_result', '0020_auto_20170605_1438'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultGeoLocation',
            fields=[
                ('latitude', models.FloatField(verbose_name='Latitude')),
                ('longitude', models.FloatField(verbose_name='Longitude')),
                ('result', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, related_name='geo_location', serialize=False, to='ndx_result.Result')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(forwards, backwards),
    ]
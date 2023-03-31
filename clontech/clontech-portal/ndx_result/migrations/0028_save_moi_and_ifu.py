# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-27 10:27
from __future__ import unicode_literals

import json

from django.db import migrations
from django.db.models import Q


def forwards(apps, schema_editor):
    Result = apps.get_model('ndx_result', 'Result')  # noqa

    for result in Result.objects.exclude(moi=None, ifu=None):
        unparsed_updated = True
        if result.unparsed_data:
            unparsed_data = json.loads(result.unparsed_data)
        else:
            unparsed_data = {}
        ndx_result = unparsed_data.get('ClontechResult', {})
        if result.moi is not None:
            if 'MOI' not in ndx_result:
                ndx_result['MOI'] = result.moi
                unparsed_updated = True
        if result.ifu is not None:
            if 'IFU' not in ndx_result:
                ndx_result['IFU'] = result.ifu
                unparsed_updated = True

        if unparsed_updated:
            unparsed_data['ClontechResult'] = ndx_result
            result.unparsed_data = json.dumps(unparsed_data)
            result.save()


def backwards(apps, schema_editor):
    Result = apps.get_model('ndx_result', 'Result')  # noqa

    for result in Result.objects.filter(
            Q(moi=None, unparsed_data__contains='"MOI":') | Q(ifu=None, unparsed_data__contains='"IFU":')):
        updated = set()
        unparsed_data = json.loads(result.unparsed_data)
        ndx_result = unparsed_data.get('ClontechResult', {})

        if result.moi is None and 'MOI' in ndx_result:
            result.moi = ndx_result.pop('MOI')
            updated.add('unparsed_data')
            updated.add('moi')
        if result.ifu is None and 'IFU' in ndx_result:
            result.ifu = ndx_result.pop('IFU')
            updated.add('unparsed_data')
            updated.add('ifu')

        if updated:
            unparsed_data['ClontechResult'] = ndx_result
            result.unparsed_data = json.dumps(unparsed_data)
            result.save(update_fields=updated)


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_result', '0027_load_gostix_value_from_unparsed_data'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]

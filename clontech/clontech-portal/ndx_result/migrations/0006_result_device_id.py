# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_result', '0005_result_reader_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='device_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
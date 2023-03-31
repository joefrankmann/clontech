# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-25 09:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_result', '0014_auto_20170523_1521'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='asset',
        ),
        migrations.RemoveField(
            model_name='result',
            name='fuel_lot_no',
        ),
        migrations.RemoveField(
            model_name='result',
            name='identity',
        ),
        migrations.RemoveField(
            model_name='result',
            name='tank_no',
        ),
        migrations.RemoveField(
            model_name='result',
            name='test_lot_no',
        ),
        migrations.AddField(
            model_name='result',
            name='reader_version',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='result',
            name='unparsed_data',
            field=models.TextField(blank=True, default='', verbose_name='Full input data in json format.'),
        ),
    ]
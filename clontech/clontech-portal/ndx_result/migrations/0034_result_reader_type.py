# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-16 11:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_result', '0033_auto_20171016_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='reader_type',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Reader type'),
        ),
    ]
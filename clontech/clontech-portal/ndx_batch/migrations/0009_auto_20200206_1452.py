# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-02-06 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_batch', '0008_auto_20200115_1256'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='assay_type',
            field=models.CharField(default='-----', max_length=64, verbose_name='Assay type'),
        ),
    ]

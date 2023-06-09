# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-31 11:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_batch', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='batch',
            options={'get_latest_by': 'valid_from', 'ordering': ('-valid_from',), 'verbose_name': 'Batch', 'verbose_name_plural': 'Batches'},
        ),
        migrations.AddField(
            model_name='batch',
            name='data_matrix',
            field=models.ImageField(blank=True, height_field='data_matrix_height', upload_to='batch/lot_no', width_field='data_matrix_width'),
        ),
        migrations.AddField(
            model_name='batch',
            name='data_matrix_height',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='batch',
            name='data_matrix_width',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='batch',
            name='lot_no',
            field=models.CharField(max_length=127, unique=True, verbose_name='Lot number'),
        ),
    ]

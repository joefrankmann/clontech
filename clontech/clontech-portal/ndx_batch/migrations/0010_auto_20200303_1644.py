# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-03-03 16:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_batch', '0009_auto_20200206_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='batch',
            name='expires',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='batch',
            name='is_active',
            field=models.BooleanField(help_text='Whether this batch is visible to users.'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_result', '0011_auto_20170523_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='teststrip',
            name='t_c_ratio',
            field=models.FloatField(default=0, verbose_name='T/C ratio'),
            preserve_default=False,
        ),
    ]
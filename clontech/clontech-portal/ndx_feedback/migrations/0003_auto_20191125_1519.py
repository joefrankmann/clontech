# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-11-25 15:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_feedback', '0002_auto_20191125_1517'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'permissions': [('view_feedback', 'Can view feedback'), ('view_feedback_emails', 'Can view users receiving feedback emails')]},
        ),
    ]

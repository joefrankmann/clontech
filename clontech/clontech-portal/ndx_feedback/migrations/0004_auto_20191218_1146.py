# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2019-12-18 11:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_feedback', '0003_auto_20191125_1519'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='feedback',
            options={'ordering': ['-created_at'], 'permissions': [('view_feedback', 'Can view feedback'), ('view_feedback_emails', 'Can view users receiving feedback emails')]},
        ),
    ]
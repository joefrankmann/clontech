# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-13 10:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_organisation', '__first__'),
        ('ndx_location', '0003_auto_20180613_0518'),
        ('ndx_auth', '0012_auto_20180606_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organisation',
            name='manager',
        ),
        migrations.RemoveField(
            model_name='organisation',
            name='parent_organisation',
        ),
        migrations.AlterField(
            model_name='ndxuser',
            name='organisation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='users', to='ndx_organisation.Organisation'),
        ),
        migrations.DeleteModel(
            name='Organisation',
        ),
    ]

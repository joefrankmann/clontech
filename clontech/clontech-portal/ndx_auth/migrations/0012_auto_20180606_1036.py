# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-06 10:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_auth', '0011_auto_20180520_1155'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organisation',
            name='address',
            field=models.TextField(default='', help_text='The full address, e.g. street, house number, city, etc. Required.', verbose_name='Address'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='parent_organisation',
            field=models.ForeignKey(blank=True, help_text='The parent organisation of this organisation. Cannot be itself.', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='child_organisations', to='ndx_auth.Organisation', verbose_name='Parent organisation'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='post_code',
            field=models.CharField(default='', max_length=30, verbose_name='Post code. Required.'),
        ),
        migrations.AlterField(
            model_name='organisation',
            name='state',
            field=models.CharField(default='', max_length=30, verbose_name='State. Required.'),
        ),
    ]

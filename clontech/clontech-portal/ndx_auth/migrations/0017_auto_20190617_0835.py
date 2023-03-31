# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-17 08:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_auth', '0016_auto_20181127_1615'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ndxuser',
            options={'default_permissions': ('add', 'change', 'delete'), 'permissions': (('view_all_orgs', 'ndx_auth.view_all_orgs'), ('change_ndxuser_password', 'ndx_auth.change_ndxuser_password'), ('edit_all_users', 'ndx_auth.edit_all_users'), ('view_all_users', 'ndx_auth.view_all_users'), ('view_user_data', 'ndx_auth.view_user_data'), ('view_ndxuser', 'view user'))},
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-27 16:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_auth', '0015_userprofile_eula_accepted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ndxuser',
            options={'permissions': [('view_ndxuser', 'ndx_auth.view_ndxuser'), ('view_all_orgs', 'ndx_auth.view_all_orgs'), ('change_ndxuser_password', 'ndx_auth.change_ndxuser_password'), ('edit_all_users', 'ndx_auth.edit_all_users'), ('view_all_users', 'ndx_auth.view_all_users'), ('view_user_data', 'ndx_auth.view_user_data')]},
        ),
    ]

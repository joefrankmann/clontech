# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-02-17 18:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_eula', '0003_auto_20200204_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eulafile',
            options={'ordering': ('locale',)},
        ),
        migrations.AlterUniqueTogether(
            name='eulafile',
            unique_together=set([('eula', 'locale')]),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-11-24 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploader_email', models.EmailField(max_length=254, verbose_name='Uploader Email')),
                ('created_at', models.DateTimeField(auto_now=True, verbose_name='Created At')),
                ('device_os', models.CharField(blank=True, default='', help_text='operating system of the device', max_length=255, verbose_name='Device OS')),
                ('device_make', models.CharField(blank=True, default='', help_text='manufacturer/brand of the device', max_length=255, verbose_name='Device Make')),
                ('device_model', models.CharField(blank=True, default='', max_length=255, verbose_name='Device Model')),
                ('device_id', models.CharField(blank=True, default='', max_length=255, verbose_name='Device ID')),
                ('app_version', models.CharField(blank=True, default='', max_length=255, verbose_name='App version')),
                ('reader_type', models.CharField(blank=True, default='', max_length=255, verbose_name='Reader type')),
                ('reader_version', models.CharField(blank=True, default='', max_length=255, verbose_name='Reader version')),
                ('rating', models.CharField(choices=[('good', 'good'), ('okay', 'okay'), ('poor', 'poor')], max_length=255, verbose_name='Rating')),
                ('follow_up', models.BooleanField(help_text='Receive a follow up on this feedback from one of our team?', verbose_name='Follow up')),
                ('comments', models.TextField(default='', help_text='General comments on the app and product', verbose_name='Comments')),
            ],
        ),
    ]

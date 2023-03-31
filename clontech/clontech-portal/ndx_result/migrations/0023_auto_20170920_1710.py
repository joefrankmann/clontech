# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 17:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ndx_result', '0022_add_batch_info_from_unparsed_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='interpretation',
            field=models.CharField(choices=[('Valid', 'Valid'), ('Positive', 'Positive'), ('Negative', 'Negative'), ('Invalid', 'Invalid')], default='Invalid', max_length=8, verbose_name='Interpretation'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 09:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_log_task_tasklog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Log',
        ),
    ]

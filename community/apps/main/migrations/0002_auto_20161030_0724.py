# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-10-30 07:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='last_alert_sent_at',
            new_name='alerts_checked_at',
        ),
    ]
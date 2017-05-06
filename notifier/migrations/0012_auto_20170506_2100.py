# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-06 21:00
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0011_auto_20170502_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='notificationrequest',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.AddField(
            model_name='notificationrequest',
            name='visited',
            field=models.IntegerField(default=0),
        ),
    ]

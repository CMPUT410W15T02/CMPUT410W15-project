# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='displayname',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='host',
            field=models.CharField(max_length=32, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='profile',
            name='uuid',
            field=models.CharField(default=uuid.uuid1, max_length=32),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_auto_20150304_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=32),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='content_type',
            field=models.CharField(default='plaintext', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='description',
            field=models.CharField(max_length=512, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=32),
            preserve_default=True,
        ),
    ]

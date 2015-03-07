# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_auto_20150305_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(upload_to=b'post_images', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=36),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=36),
            preserve_default=True,
        ),
    ]

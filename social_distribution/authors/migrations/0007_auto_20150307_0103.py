# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0006_auto_20150304_2002'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='github',
            field=models.CharField(max_length=39, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=36),
            preserve_default=True,
        ),
    ]

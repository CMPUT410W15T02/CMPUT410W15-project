# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_auto_20150301_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=32),
            preserve_default=True,
        ),
    ]

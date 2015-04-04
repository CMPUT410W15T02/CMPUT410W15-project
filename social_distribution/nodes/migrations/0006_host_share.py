# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0005_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='share',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]

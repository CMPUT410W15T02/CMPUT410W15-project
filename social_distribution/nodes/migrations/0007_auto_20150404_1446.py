# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0006_host_share'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='share',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

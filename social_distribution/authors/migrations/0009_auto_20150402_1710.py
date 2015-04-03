# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0008_auto_20150328_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='host',
            field=models.CharField(max_length=64, blank=True),
            preserve_default=True,
        ),
    ]

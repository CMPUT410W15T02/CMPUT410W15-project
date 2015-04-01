# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0003_auto_20150320_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='password',
            field=models.CharField(default='password', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='host',
            name='username',
            field=models.CharField(default='username', max_length=64),
            preserve_default=False,
        ),
    ]

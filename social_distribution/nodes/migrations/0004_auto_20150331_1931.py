# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0003_auto_20150320_1929'),
    ]

    operations = [
        migrations.AddField(
            model_name='host',
            name='password',
            field=models.CharField(default=datetime.datetime(2015, 4, 1, 1, 31, 13, 829241, tzinfo=utc), max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='host',
            name='username',
            field=models.CharField(default=datetime.datetime(2015, 4, 1, 1, 31, 19, 675189, tzinfo=utc), max_length=64),
            preserve_default=False,
        ),
    ]

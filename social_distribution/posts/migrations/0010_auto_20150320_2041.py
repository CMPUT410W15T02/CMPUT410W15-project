# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_auto_20150320_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(max_length=32, choices=[(b'text/plain', b'Plain text'), (b'text/x-markdown', b'Markdown'), (b'text/html', b'HTML')]),
            preserve_default=True,
        ),
    ]

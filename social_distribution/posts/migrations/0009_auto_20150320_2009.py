# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20150307_1933'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(max_length=16, choices=[(b'plaintext', b'text/plain'), (b'markdown', b'text/x-markdown'), (b'html', b'text/html')]),
            preserve_default=True,
        ),
    ]

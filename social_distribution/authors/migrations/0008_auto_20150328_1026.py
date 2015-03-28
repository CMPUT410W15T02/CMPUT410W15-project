# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0007_auto_20150307_0103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='status',
            field=models.CharField(max_length=10, choices=[(b'FOLLOWING', b'Following'), (b'PENDING', b'Pending')]),
            preserve_default=True,
        ),
    ]

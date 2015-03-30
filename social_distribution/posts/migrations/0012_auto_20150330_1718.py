# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_auto_20150328_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.CharField(max_length=1, choices=[(b'1', b'Public'), (b'2', b'Private'), (b'3', b'Friend of a Friend'), (b'4', b'Friend on this Server'), (b'5', b'Friend on this Server')]),
            preserve_default=True,
        ),
    ]

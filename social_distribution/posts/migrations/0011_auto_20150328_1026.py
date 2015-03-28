# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20150320_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='allowed',
            field=models.ManyToManyField(related_name='allowed', null=True, to='authors.Profile', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='privacy',
            field=models.CharField(max_length=1, choices=[(b'1', b'Public'), (b'2', b'Private'), (b'3', b'Friend of a Friend'), (b'4', b'Friends')]),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20150227_2159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='allowed',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(to='authors.Profile'),
            preserve_default=True,
        ),
    ]

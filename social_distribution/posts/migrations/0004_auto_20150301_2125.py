# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_auto_20150228_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.OneToOneField(to='authors.Profile'),
            preserve_default=True,
        ),
    ]

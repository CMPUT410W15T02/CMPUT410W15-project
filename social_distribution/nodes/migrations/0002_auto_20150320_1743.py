# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='host',
            old_name='posts_visisble_to_current_user',
            new_name='posts_visible_to_current_user',
        ),
    ]

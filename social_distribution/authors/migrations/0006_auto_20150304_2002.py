# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0005_remove_profile_follows'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(max_length=10, choices=[(b'REJECTED', b'Rejected'), (b'PENDING', b'Pending')])),
                ('from_profile_id', models.ForeignKey(related_name='from_profile_id', to='authors.Profile')),
                ('to_profile_id', models.ForeignKey(related_name='to_profile_id', to='authors.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='profile',
            name='follows',
            field=models.ManyToManyField(to='authors.Profile', through='authors.Follow', blank=True),
            preserve_default=True,
        ),
    ]

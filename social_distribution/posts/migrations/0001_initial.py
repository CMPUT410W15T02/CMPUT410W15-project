# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(max_length=2048)),
                ('date', models.DateTimeField(verbose_name=b'date posted')),
                ('author', models.OneToOneField(to='authors.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_text', models.TextField(max_length=2048)),
                ('title', models.CharField(max_length=128, blank=True)),
                ('date', models.DateTimeField(verbose_name=b'date posted')),
                ('privacy', models.CharField(max_length=1, blank=True)),
                ('author', models.OneToOneField(to='authors.Profile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='comment',
            name='post_id',
            field=models.ForeignKey(to='posts.Post'),
            preserve_default=True,
        ),
    ]

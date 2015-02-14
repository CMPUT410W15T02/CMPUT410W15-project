# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=128)),
                ('password', models.CharField(max_length=128)),
                ('follows', models.ManyToManyField(to='authors.Author', blank=True)),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='authors.Author', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'N/A', max_length=128)),
                ('body', models.CharField(max_length=2048, blank=True)),
                ('birthdate', models.DateField(null=True, verbose_name=b'birthdate', blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('image', models.ImageField(upload_to=b'', blank=True)),
                ('workspace', models.CharField(max_length=128, blank=True)),
                ('school', models.CharField(max_length=128, blank=True)),
                ('author_id', models.ForeignKey(to='authors.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

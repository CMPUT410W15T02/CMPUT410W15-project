# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField(max_length=2048, blank=True)),
                ('birthdate', models.DateField(null=True, verbose_name=b'birthdate', blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('image', models.ImageField(upload_to=b'profile_images', blank=True)),
                ('workspace', models.CharField(max_length=128, blank=True)),
                ('school', models.CharField(max_length=128, blank=True)),
                ('follows', models.ManyToManyField(to='authors.Profile', blank=True)),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='authors.Profile', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

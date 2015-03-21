# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('host_url', models.CharField(max_length=128)),
                ('posts_visisble_to_current_user', models.CharField(default=b'/author/posts', max_length=64)),
                ('public_posts', models.CharField(default=b'/posts', max_length=64)),
                ('all_posts_by_author_visible', models.CharField(default=b'/author/{AUTH_ID}/posts', max_length=64)),
                ('get_put_post_postid', models.CharField(default=b'/posts/{POST_ID}', max_length=64)),
                ('friend_response', models.CharField(default=b'/friends/{AUTH1_ID}/{AUTH2_ID}', max_length=64)),
                ('friend_auth_response', models.CharField(default=b'/friends/{AUTH_ID}', max_length=64)),
                ('friend_request', models.CharField(default=b'/friendrequest', max_length=64)),
                ('all_authors', models.CharField(default=b'/authors', max_length=64)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

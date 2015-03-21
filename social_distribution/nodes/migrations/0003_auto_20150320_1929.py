# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0002_auto_20150320_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='all_authors',
            field=models.CharField(default=b'/authors/', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='all_posts_by_author_visible',
            field=models.CharField(default=b'/author/{AUTH_ID}/posts/', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='friend_auth_response',
            field=models.CharField(default=b'/friends/{AUTH_ID}/', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='friend_request',
            field=models.CharField(default=b'/friendrequest/', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='friend_response',
            field=models.CharField(default=b'/friends/{AUTH1_ID}/{AUTH2_ID}/', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='get_put_post_postid',
            field=models.CharField(default=b'/posts/{POST_ID}/', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='posts_visible_to_current_user',
            field=models.CharField(default=b'/author/posts/', max_length=64),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='public_posts',
            field=models.CharField(default=b'/posts/', max_length=64),
            preserve_default=True,
        ),
    ]

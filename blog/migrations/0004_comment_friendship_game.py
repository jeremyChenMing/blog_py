# Generated by Django 2.2.3 on 2019-09-19 08:04

import blog.utils.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190918_1745'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.CharField(default=blog.utils.models.gen_uuid, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('kilometer', models.IntegerField(default=0)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='game_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FriendShip',
            fields=[
                ('id', models.CharField(default=blog.utils.models.gen_uuid, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('followed', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='followed', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.CharField(default=blog.utils.models.gen_uuid, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('word', models.TextField()),
                ('to_comment', models.CharField(default='', max_length=36)),
                ('belong_artical', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='artical_comment', to='blog.Artical')),
                ('belong_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# Generated by Django 3.1.5 on 2021-01-26 22:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('channel_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=2000)),
                ('music', models.CharField(max_length=1000000000)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('song_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=2000)),
                ('singer', models.CharField(max_length=2000)),
                ('description', models.TextField(default='')),
                ('tags', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='images')),
                ('song', models.FileField(upload_to='images')),
                ('movie', models.CharField(default='', max_length=1000)),
                ('credit', models.CharField(default='', max_length=10000)),
            ],
        ),
        migrations.CreateModel(
            name='WatchLater',
            fields=[
                ('watch_id', models.AutoField(primary_key=True, serialize=False)),
                ('video_id', models.CharField(default='', max_length=10000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='userExtended',
            fields=[
                ('userExtended_id', models.AutoField(primary_key=True, serialize=False)),
                ('picture', models.ImageField(upload_to='images')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('hist_id', models.AutoField(primary_key=True, serialize=False)),
                ('music_id', models.CharField(default='', max_length=10000000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

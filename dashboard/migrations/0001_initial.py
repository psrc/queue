# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import dashboard.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InputConfigurationValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=240, db_index=True)),
                ('value', models.CharField(max_length=240, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='InputTypeDict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, db_index=True)),
                ('cpus', models.PositiveIntegerField(default=1)),
                ('ram_gb', models.PositiveIntegerField(db_index=True)),
                ('scratch_path', models.CharField(max_length=512, db_index=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, db_index=True)),
                ('project_contact', models.CharField(max_length=256, db_index=True)),
                ('modeling_contact', models.CharField(max_length=256, db_index=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='RunLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project', models.CharField(max_length=128, null=True, verbose_name=dashboard.models.Project)),
                ('series', models.CharField(max_length=3, blank=True)),
                ('note', models.CharField(max_length=2048, blank=True)),
                ('status', models.IntegerField(default=-1, db_index=True)),
                ('start', models.DateTimeField(auto_now_add=True, verbose_name=b'started')),
                ('duration', models.DurationField(null=True, blank=True)),
                ('tool_tag', models.CharField(db_index=True, max_length=64, verbose_name=b'tag', blank=True)),
                ('inputs', models.CharField(max_length=2048, blank=True)),
            ],
            options={
                'ordering': ['-start'],
            },
        ),
        migrations.CreateModel(
            name='SoundcastRuns',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('runid', models.CharField(max_length=240, db_index=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tool',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, db_index=True)),
                ('url', models.CharField(max_length=1024)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('website', models.URLField(blank=True)),
                ('picture', models.ImageField(upload_to=b'profile_image', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='runlog',
            name='tool',
            field=models.ForeignKey(to='dashboard.Tool'),
        ),
        migrations.AddField(
            model_name='runlog',
            name='user',
            field=models.ForeignKey(related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='node',
            name='tools',
            field=models.ManyToManyField(to='dashboard.Tool'),
        ),
        migrations.AddField(
            model_name='inputconfigurationvalue',
            name='container',
            field=models.ForeignKey(to='dashboard.InputTypeDict'),
        ),
    ]

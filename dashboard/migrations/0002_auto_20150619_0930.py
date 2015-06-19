# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='runlog',
            name='project',
            field=models.CharField(max_length=128, null=True, verbose_name=b'project'),
        ),
    ]

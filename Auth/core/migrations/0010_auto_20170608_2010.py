# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_event_game'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.CharField(null=True, max_length=128, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='notes',
            field=models.CharField(null=True, max_length=32, blank=True),
        ),
    ]

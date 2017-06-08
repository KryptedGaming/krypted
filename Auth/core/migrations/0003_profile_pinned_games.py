# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170607_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='pinned_games',
            field=models.ManyToManyField(related_name='pinned', to='core.Game'),
        ),
    ]

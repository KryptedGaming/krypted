# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('core', '0008_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='game',
            field=models.ForeignKey(blank=True, to='auth.Group', null=True),
        ),
    ]

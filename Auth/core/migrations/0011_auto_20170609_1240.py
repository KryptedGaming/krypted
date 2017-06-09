# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20170608_2010'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='game',
            new_name='group',
        ),
    ]

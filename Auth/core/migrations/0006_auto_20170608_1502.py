# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170608_1440'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='blizard',
            new_name='blizzard',
        ),
    ]

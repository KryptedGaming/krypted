# Generated by Django 2.0.3 on 2018-04-21 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('discord', '0002_auto_20180421_1700'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DiscordRole',
            new_name='DiscordGroup',
        ),
        migrations.RenameField(
            model_name='discordgroup',
            old_name='role_id',
            new_name='id',
        ),
    ]
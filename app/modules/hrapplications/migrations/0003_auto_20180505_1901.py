# Generated by Django 2.0.3 on 2018-05-05 19:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrapplications', '0002_auto_20180505_1740'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'permissions': (('view_applications', 'Can view all applications'), ('view_application', 'Can view individual applications'), ('audit_eve_application', 'Can audit an EVE application'), ('approve_application', 'Can approve an application'), ('deny_application', 'Can deny an application'))},
        ),
    ]
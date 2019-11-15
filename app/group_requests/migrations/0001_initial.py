# Generated by Django 2.2.4 on 2019-11-15 19:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='ClosedGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth.Group')),
            ],
        ),
        migrations.CreateModel(
            name='GroupRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_date', models.DateField(auto_now=True)),
                ('response_action', models.CharField(choices=[('PENDING', 'Pending'), ('ACCEPTED', 'Accepted'), ('REJECTED', 'Rejected'), ('RETRACTED', 'Retracted')], default='PENDING', max_length=32)),
                ('response_date', models.DateField(blank=True, null=True)),
                ('request_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='group_requests', to='auth.Group')),
                ('request_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='grouprequests_submitted', to=settings.AUTH_USER_MODEL)),
                ('response_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='grouprequests_managed', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': [('bypass_group_requirement', 'Can approve, reject, and view groups despite not being in them.')],
                'unique_together': {('request_user', 'request_group')},
            },
        ),
    ]

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

# START
app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# CONFIGURATION
app.conf.broker_url='amqp://localhost'
app.conf.task_default_queue='default'
app.conf.accept_content=['application/json']
app.conf.result_serializer='json'
app.conf.task_serializer='json'
app.conf.timezone='UTC'

"""
ROUTES
When using multiple queues and workers, be sure to redirect properly.
e.g ('modules.discord.tasks.*', {'queue': 'discord_development'}),
"""
app.conf.routes=([
    ('modules.discord.tasks.*', {'queue': 'discord'}),
    ('modules.discourse.tasks.*', {'queue': 'discourse'}),
])

"""
SCHEDULE
Task schedules go here.
"""
app.conf.beat_schedule = {
    'update_sso_tokens' : {
        'task': 'modules.eveonline.tasks.update_sso_tokens',
        'schedule': 3600.0
    },
    'update_eve_characters': {
        'task': 'modules.eveonline.tasks.update_eve_characters',
        'schedule': 3600.0
    },
    'update_eve_character_corporations': {
        'task': 'modules.eveonline.tasks.update_eve_character_corporations',
        'schedule': 3600.0
    },
    'update_discord_users': {
        'task': 'modules.discord.tasks.update_discord_users',
        'schedule': 3600.0
    },
    'audit_eve_group_integrations': {
        'task': 'modules.eveonline.tasks.audit_eve_group_integrations',
        'schedule': 3600.0
    }
}

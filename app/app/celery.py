import os
import celery
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

app = Celery('app')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# CONFIGURATION
app.conf.broker_url = os.environ.get('REDIS_HOST', 'redis://redis:6379/0') # redis://localhost:6379/0 for development
app.conf.accept_content = ['application/json']
app.conf.result_serializer = 'json'
app.conf.task_serializer = 'json'
app.conf.timezone = 'UTC'

@celery.signals.setup_logging.connect
def on_setup_logging(**kwargs):
    pass
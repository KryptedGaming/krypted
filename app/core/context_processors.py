from django.conf import settings
from django.apps import apps
from core.models import SocialMedia

def installed_apps(request):
    return {
       'installed_apps' : settings.INSTALLED_APPS
    }

def social_media_objects(request):
    return {
        'social_media_objects': SocialMedia.objects.all()
    }

def get_application_verbose_names(request):
    applications = {}
    if apps.is_installed('modules.guilds'):
        applications['guilds'] = apps.get_app_config('guilds').verbose_name
    return {
        'application_verbose_names': applications
    }

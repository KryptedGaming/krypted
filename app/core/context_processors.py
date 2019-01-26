from django.conf import settings
from core.models import SocialMedia

def installed_apps(request):
    return {
       'installed_apps' : settings.INSTALLED_APPS_WITH_CONFIGS + settings.INSTALLED_APPS
    }

def social_media_objects(request):
    return {
        'social_media_objects': SocialMedia.objects.all()
    }

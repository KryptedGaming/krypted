from django.conf import settings
from django.apps import apps
from core.models import SocialMedia

core_settings = apps.get_app_config('core')

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

def get_google_analytics_code(request):
    return {
        'GOOGLE_ANALYTICS_CODE': core_settings.GOOGLE_ANALYTICS_CODE
    }

def get_site_logo(request):
    return {
        'SITE_LOGO': core_settings.SITE_LOGO
    }

def get_site_title(request):
    return {
        'SITE_TITLE': core_settings.SITE_TITLE
    }

def get_breadcrumbs(request):
    from django.urls import reverse, NoReverseMatch
    identifiers = request.get_full_path().split("/")
    breadcrumbs = []
    for identifier in identifiers:
        try:
            reverse(identifier)
            breadcrumbs.append(identifier)
        except NoReverseMatch:
            pass
    return {
        'breadcrumbs': breadcrumbs
    }

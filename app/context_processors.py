from django.conf import settings


def installed_apps(request):
    return {
        'INSTALLED_APPS': settings.INSTALLED_APPS
    }

from django.conf import settings
import django

def installed_apps(request):
    return {
        'INSTALLED_APPS': settings.INSTALLED_APPS
    }

def site_logo(request):
    return {
        'SITE_LOGO': settings.SITE_LOGO
    }

def google_analytics(request):
    return {
        'GOOGLE_ANALYTICS': settings.GOOGLE_ANALYTICS
    }

def site_name(request):
    return {
        'SITE_NAME': settings.SITE_TITLE
    }

def version(request):
    return {
        'VERSION': __import__("app").__version__
    }
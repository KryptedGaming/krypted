from django.conf import settings
import django

def installed_apps(request):
    return {
        'INSTALLED_APPS': settings.INSTALLED_APPS
    }

def sidebar_extensions(request):
    templates = []
    for EXTENSION in settings.EXTENSIONS:
        template_name = "%s/sidebar.html" % EXTENSION.lower()
        try: 
            django.template.loader.get_template(template_name) 
            templates.append(template_name)
        except Exception as e:
            pass 

    return {
        'SIDEBAR_EXTENSIONS': templates
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
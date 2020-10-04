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


def site_name(request):
    return {
        'SITE_NAME': settings.SITE_TITLE
    }

from django.conf import settings
import django

def installed_apps(request):
    return {
        'INSTALLED_APPS': settings.INSTALLED_APPS
    }

def sidebar_extensions(request):
    templates = []
    for KRYPTED_APP in settings.KRYPTED_APPS:
        template_name = "%s/sidebar.html" % KRYPTED_APP.lower()
        try: 
            django.template.loader.get_template(template_name) 
            templates.append(template_name)
        except Exception as e:
            pass 

    return {
        'SIDEBAR_EXTENSIONS': templates
    }
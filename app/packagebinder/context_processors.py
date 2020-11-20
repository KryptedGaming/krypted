import django
from django.apps import apps 


def extension_versions(request):
    setup_definitions = []
    setup_files = []
    for EXTENSION in settings.EXTENSIONS:
        try:
            name = __import__(EXTENSION.lower()).__package_name__
        except Exception as e:
            continue

        try:
            current_version = __import__(EXTENSION.lower()).__version__
        except Exception as e:
            current_version = 'UNKNOWN'

        try:
            github_url = __import__(EXTENSION.lower()).__url__
        except Exception as e:
            github_url = None

        setup_definitions.append({
            'name': name,
            'current_version': current_version,
            'github_url': github_url,
        })

    return {
        'EXTENSION_VERSIONS': setup_definitions
    }


def sidebar_bindings(request):
    sidebar_bindings = apps.get_app_config('packagebinder').sidebar_bindings
    parsed_sidebar_bindings = []
    for sidebar_binding in sidebar_bindings.keys():
        parsed_sidebar_bindings.append(sidebar_bindings[sidebar_binding])

    return {
        'SIDEBAR_BINDINGS': parsed_sidebar_bindings
    }

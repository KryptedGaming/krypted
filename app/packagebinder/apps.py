from django.apps import AppConfig
from .exceptions import BindException

class PackagebinderConfig(AppConfig):
    name = 'packagebinder'
    url_slug = 'setup'

    package_bindings = []
    settings_bindings = []
    task_bindings = []
    sidebar_bindings = {}
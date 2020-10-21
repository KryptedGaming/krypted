from django.apps import AppConfig
from .exceptions import BindException

class PackagebinderConfig(AppConfig):
    name = 'packagebinder'
    url_slug = 'setup'
    package_bindings = []


    @staticmethod
    def get_bind_object(package_name, version):
        from packagebinder.bind import BindObject 
        bind = BindObject(package_name, version)
        return bind 

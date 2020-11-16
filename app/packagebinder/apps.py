from django.apps import AppConfig
from .exceptions import BindException

class PackagebinderConfig(AppConfig):
    name = 'packagebinder'
    url_slug = 'setup'
    package_bindings = []


    @staticmethod
    def get_bind_object(package_name, version):
        from packagebinder.bind import BindObject 
        from django_celery_beat.models import PeriodicTask
        # check if we're not in a migration 
        try:
            PeriodicTask.objects.all()
        except Exception as e:
            print(e)
            raise BindException("Cannot bind at this time")
        bind = BindObject(package_name, version)
        return bind 
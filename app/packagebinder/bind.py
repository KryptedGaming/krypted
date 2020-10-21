from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.db.utils import OperationalError
from .exceptions import BindException
from django.apps import apps 

class BindObject():
    def __init__(self, package_name, version):
        self.package_name = package_name
        self.version = version 
        self.required_tasks = []
        self.optional_tasks = [] 
    
    def __str__(self):
        return self.package_name

    def refresh(self):
        for task in self.required_tasks:
            task.refresh_from_db()
        for task in self.optional_tasks:
            task.refresh_from_db()

    def save(self):
        binder_config = apps.get_app_config('packagebinder')
        binder_config.package_bindings.append(self)
        
    def add_required_task(self, name, task, interval, interval_period):
        try:
            interval = IntervalSchedule.objects.get_or_create(
                every=interval, period=interval_period)[0]
        except OperationalError:
            raise BindException("Failed to add required task, likely in database migration")
        except Exception as e:
            interval = IntervalSchedule.objects.filter(every=interval, period=interval_period).first()

        if not PeriodicTask.objects.filter(name=name).exists():
            periodic_task = PeriodicTask.objects.create(name=name, 
                                task=task, 
                                interval=interval,
                                enabled=True)
        else:
            periodic_task =  PeriodicTask.objects.get(name=name)

        self.required_tasks.append(periodic_task)

    def add_optional_task(self, name, task, interval, interval_period):
        try:
            interval = IntervalSchedule.objects.get_or_create(
                every=interval, period=interval_period)[0]
        except OperationalError:
            raise BindException("Failed to add required task, likely in database migration")
        except Exception as e:
            interval = IntervalSchedule.objects.filter(every=interval, period=interval_period).first()


        if not PeriodicTask.objects.filter(name=name).exists():
            periodic_task = PeriodicTask.objects.create(name=name,
                                                        task=task,
                                                        interval=interval,
                                                        enabled=False)
        else:
            periodic_task = PeriodicTask.objects.get(name=name)

        self.optional_tasks.append(periodic_task)


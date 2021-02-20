from django_celery_beat.models import PeriodicTask, IntervalSchedule
from django.db.utils import OperationalError, ProgrammingError
from .exceptions import BindException
from django.apps import apps
import logging
logger = logging.getLogger(__name__)

package_config = apps.get_app_config('packagebinder')


class PackageBinding():
    def __init__(self, package_name, version, url_slug):
        self.package_name = package_name
        self.version = version
        self.url_slug = url_slug

    def save(self):
        package_config.package_bindings.append(self)


class SettingsBinding():
    def __init__(self, package_name, settings_class, settings_form):
        self.package_name = package_name
        self.settings_class = settings_class
        self.settings_form = settings_form
        self.settings_form_instance = settings_form()
        self.is_valid = False

    def refresh(self):
        try:
            self.settings_form_instance = self.settings_form(
                instance=self.settings_class.get_instance())
            self.is_valid = True
        except Exception as e:
            self.settings_form_instance = self.settings_form()
            self.is_valid = False

    def save(self):
        package_config.settings_bindings.append(self)


class TaskBinding():
    def __init__(self, package_name, required_tasks, optional_tasks):
        self.package_name = package_name
        self.required_tasks = []
        self.optional_tasks = []
        for task in required_tasks:
            task_object = self.add_task(
                task['name'], task['task_name'], task['interval'], task['interval_period'])
            if task_object:
                self.required_tasks.append(task_object)
        for task in optional_tasks:
            task_object = self.add_task(
                task['name'], task['task_name'], task['interval'], task['interval_period'], True)
            if task_object:
                self.optional_tasks.append(task_object)

    def refresh(self):
        for task in self.required_tasks:
            task.refresh_from_db()
        for task in self.optional_tasks:
            task.refresh_from_db()

    def add_task(self, name, task, interval, interval_period, optional=False):
        try:
            if IntervalSchedule.objects.filter(every=interval, period=interval_period).exists():
                interval = IntervalSchedule.objects.filter(
                    every=interval, period=interval_period).first()
            else:
                interval = IntervalSchedule.objects.create(
                    every=interval, period=interval_period)
        except ProgrammingError:
            logger.warning(
                f"{name}: Failed to add task binding ({task}), likely during database migration.")
            return None
        except OperationalError:
            logger.warning(
                f"{name}: Failed to add task binding ({task}), likely during database migration.")
            return None
        except Exception as e:
            raise BindException(f"Failed to add task binding: {e}")
            return None

        if not PeriodicTask.objects.filter(name=name).exists():
            periodic_task = PeriodicTask.objects.create(name=name,
                                                        task=task,
                                                        interval=interval,
                                                        enabled=not optional)
        else:
            periodic_task = PeriodicTask.objects.get(name=name)

        return periodic_task

    def save(self):
        package_config.task_bindings.append(self)


class SidebarBinding():
    def __init__(self, package_name, parent_menu_item, child_menu_items):
        self.package_name = package_name
        self.parent_menu_item = parent_menu_item
        self.children_menu_items = child_menu_items

    def save(self):
        package_config.sidebar_bindings[self.package_name] = self

    def add_child_menu_item(self, item):
        self.children_menu_items.append(item)

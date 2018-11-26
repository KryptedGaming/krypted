from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

UserModel = get_user_model()

class KryptedBackend(ModelBackend):
    def _get_group_permissions(self, user_obj):
        return Permission.objects.filter(group__in=user_obj.groups.all())

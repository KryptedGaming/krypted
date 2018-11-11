from django.conf import settings
from django.contrib.auth.hashers import check_password
from core.models import User

class KryptedAuthentication():
    def authenticate(request, username, password):
        try:
            user=User.objects.get(username=username)
            print("ok")
            success=check_password(user.password, password)
            print("ok")
            print(success)
            if success:
                return user
        except User.DoesNotExist:
                return None

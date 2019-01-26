# DJANGO
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
# INTERNAL
from core.models import *
# MISC
import uuid


def username_or_email_resolver(username):
    if User.objects.filter(email=username).exists():
        return User.objects.get(email=username).username
    else:
        return username
def send_activation_email(user):
    user.info.activation_key = uuid.uuid4()
    user.save()
    send_mail(
        'Verify your Krypted Account',
        'Welcome to Krypted Gaming. \n Please click the following link to verify your account. \n' + settings.SERVER_DOMAIN + '/verify/confirmation/' + str(user.info.activation_key),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False
    )

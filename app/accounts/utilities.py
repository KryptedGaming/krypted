from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail


def username_or_email_resolver(username):
    if User.objects.filter(email=username).exists():
        return User.objects.get(email=username).username
    else:
        return username


def send_activation_email(user):
    send_mail(
        'Verify your Krypted account',
        'Welcome to %s. \n Please click the following link to verify your account. \n %s/accounts/activate/%s' % (
            settings.SITE_TITLE, settings.SITE_URL, user.info.secret),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False)

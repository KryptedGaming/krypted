from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User, Group
import datetime
import logging

logger = logging.getLogger(__name__)

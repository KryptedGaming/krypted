from core.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
import logging

logger = logging.getLogger(__name__)

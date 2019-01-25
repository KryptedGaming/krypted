from django.apps import AppConfig
from django.db.models.signals import m2m_changed
"""
Records Application

Dependencies
    - core

Purpose: Create an audit trail for core activities
"""


class RecordsConfig(AppConfig):
    name = 'modules.records'

    def ready(self):
        from modules.engagement.models import Event
        from django.contrib.auth.models import User
        from modules.records.signals import event_registrants_change, event_participants_change
        m2m_changed.connect(event_participants_change, sender=Event.participants.through)
        m2m_changed.connect(event_registrants_change, sender=Event.registrants.through)

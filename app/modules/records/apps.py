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
        from core.models import User, Event
        from modules.records.signals import event_registrants_change, event_participants_change, user_guilds_change
        m2m_changed.connect(event_participants_change, sender=Event.participants.through)
        m2m_changed.connect(event_registrants_change, sender=Event.registrants.through)
        m2m_changed.connect(user_guilds_change, sender=User.guilds.through)

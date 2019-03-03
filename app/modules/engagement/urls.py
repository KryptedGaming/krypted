
from django.conf.urls import include, url
from .views import events, surveys
from . import feeds

urlpatterns = []

# EVENTS
urlpatterns += [
    url(r'^events/$', events.dashboard, name='events'),
    url(r'^events/view/(?P<pk>\d+)/$', events.view_event, name='view-event'),
    url(r'^events/add/$', events.add_event, name='add-event'),
    url(r'^events/edit/(?P<pk>\d+)/$', events.edit_event, name='edit-event'),
    url(r'^events/edit/(?P<event_pk>\d+)/add/registrant/$', events.add_event_registrant, name='edit-event-add-registrant'),
    url(r'^events/edit/(?P<event_pk>\d+)/remove/registrant/$', events.remove_event_registrant, name='edit-event-remove-registrant'),
    url(r'^events/edit/(?P<event_pk>\d+)/add/participant/$', events.add_event_participant, name='edit-event-add-participant'),
    url(r'^events/remove/(?P<pk>\d+)/$', events.remove_event, name='remove-event'),
    url(r'^events/calendar.ics$', feeds.EventFeed(), name='sync-events'),
]

## SURVEYS
urlpatterns += [
    url(r'^surveys/$', surveys.dashboard, name='surveys'),
    url(r'^surveys/view/(?P<pk>\d+)/$', surveys.view_survey, name='view-survey'),
    url(r'^surveys/redirect/(?P<pk>\d+)/$', surveys.redirect_to_survey, name='redirect-survey'),
    url(r'^surveys/complete/(?P<pk>\d+)/$', surveys.complete_survey, name='complete-survey'),
]

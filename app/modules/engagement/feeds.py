from django_ical.views import ICalFeed
from django.contrib.auth.models import User, Group
from modules.engagement.models import Event

class EventFeed(ICalFeed):
    """
    A simple event calender
    """
    product_id = '-//example.com//Example//EN'
    timezone = 'UTC'
    file_name = "event.ics"

    def __call__(self, request, *args, **kwargs):
        self.request = request
        return super(EventFeed, self).__call__(request, *args, **kwargs)

    def items(self):
        if 'secret' in self.request.GET and 'user' in self.request.GET:
            user = User.objects.get(info__secret=self.request.GET['secret'], pk=self.request.GET['user'])
            user_groups = Group.objects.all().filter(user__in=[user])
            user_events = Event.objects.filter(group__in=user_groups);
        else:
            user_events = Event.objects.filter(group=None)
        return user_events.union(Event.objects.filter(group=None)).order_by('-start_datetime')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return item.start_datetime

    def item_end_datetime(self, item):
        return item.end_datetime

from django_ical.views import ICalFeed
from core.models import Event, User

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
            user = User.objects.get(secret=self.request.GET['secret'], pk=self.request.GET['user'])
            user_guilds = user.guilds.all()
            user_events = Event.objects.filter(guild__in=user_guilds);
        else:
            user_events = Event.objects.filter(guild=None)
        return user_events.union(Event.objects.filter(guild=None)).order_by('-start_datetime')

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_start_datetime(self, item):
        return item.start_datetime

    def item_end_datetime(self, item):
        return item.end_datetime

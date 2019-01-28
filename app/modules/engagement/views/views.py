# DJANGO IMPORTS
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.apps import apps
# CRISPY FORMS IMPORTS
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit, Button
from crispy_forms.bootstrap import *
# INTERAL IMPORTS
from modules.engagement.models import Event, Survey
# MISC
import logging, datetime, pytz, uuid, random

logger = logging.getLogger(__name__)
class BoxedField(Field):
    template='crispy_template/field.html'
    def __init__(self,*args,**kwargs):
        super(BoxedField,self).__init__(*args,**kwargs)

class EventCreate(CreateView):
    template_name='events/add_event.html'
    model = Event
    fields = ['name','group','description','start_datetime', 'end_datetime'];
    success_url = reverse_lazy('all-events')

    def form_valid(self,form):
        # The user that creates the Event is the owner
        user = self.request.user
        form.instance.user = user
        form.instance.password = random.randint(100,999)
        return super(EventCreate,self).form_valid(form)

    def get_form(self, form_class=None):
        form = super(EventCreate, self).get_form(form_class)
        form.helper = FormHelper()
        form.helper.form_method = 'POST'
        onclick = "location.href='%s'" % reverse_lazy('all-events')
        form.helper.layout = Layout(
            *[BoxedField(f) for f in self.fields],
            FormActions(
                Submit('Create Event','Create Event', css_class='btn-success'),
                Button('Cancel','Cancel', css_class='btn-danger', onclick=onclick)
            )
        )
        form.fields['group'].queryset = self.request.user.groups.all()
        return form

class EventUpdate(UpdateView):
    model = Event
    fields = ['name', 'description', 'start_datetime', 'end_datetime']
    template_name = "events/edit_event.html"
    success_url = reverse_lazy('all-events')
    def get_form(self, form_class=None):
        form = super(EventUpdate, self).get_form(form_class)
        form.helper = FormHelper()
        form.helper.form_method = 'POST'
        onclick = "location.href='%s'" % reverse_lazy('all-events')
        form.helper.layout = Layout(
            *[BoxedField(f) for f in self.fields],
            FormActions(
                Submit('Modify Event','Modify Event', css_class='btn-warning'),
                Button('Cancel','Cancel', css_class='btn-danger', onclick=onclick)
            )
        )
        return form

class EventDelete(DeleteView):
    model = Event
    success_url = reverse_lazy('all-events')
    template_name = "events/delete_event.html"

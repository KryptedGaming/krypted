from django import template
from django import forms, template
register = template.Library()

@register.filter(name='is_datetime')
def is_datetime(field):
    return isinstance(field.field.widget,forms.DateTimeInput)

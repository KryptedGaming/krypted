from django import template
from django.template.defaultfilters import stringfilter
register = template.Library()

@register.filter(name='choiceBuilder')
def choiceBuilder(string):
    string = string.split(",")
    return string

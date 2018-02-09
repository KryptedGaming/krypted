from django import template
from django.template.defaultfilters import stringfilter
import re
register = template.Library()

@register.filter(name='cleanTypes')
def cleanTypes(string):
    string = string.split("_")
    cleaned_value = ""
    for data in string:
        cleaned_value += data.title() + " "
    return cleaned_value

@register.filter(name='eveWhoConverter')
def eveWhoConverter(string):
    string = string.replace(' ', '+')
    url = "https://evewho.com/pilot/" + string
    return url

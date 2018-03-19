from django import template
register = template.Library()

@register.filter(name='cleanGroupName')
def cleanGroupName(string):
    string = string.replace('-', ' ')
    return string

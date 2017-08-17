from django import template
register = template.Library()

@register.filter(name='c_create')
def coordinator_create(user):
    if user.has_perm('core.add_event'):
        return True
    else:
        return False

@register.filter(name='c_modify')
def coordinator_modify(user):
    if user.has_perm('core.change_event'):
        return True
    else:
        return False

@register.filter(name='c_delete')
def coordinator_delete(user):
    if user.has_perm('core.delete_event'):
        return True
    else:
        return False

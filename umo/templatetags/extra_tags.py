from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    return Group.objects.get(name=group_name) in user.groups.all()

@register.filter
def get_list(group_dict, edu_program):
    return ', '.join(group_dict[edu_program.id]) if edu_program else ''

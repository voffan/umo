from django import template
from django.contrib.auth.models import Group

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name): 
    return Group.objects.get(name=group_name) in user.groups.all()

@register.filter
def get_maxpoint(max_points, checkpoint):
    return str(max_points[checkpoint.id]) if checkpoint.id in max_points.keys() else ''

@register.filter
def get_list(group_dict, edu_program):
    if edu_program.id in group_dict.keys():
        return ', '.join(group_dict[edu_program.id]) if edu_program else ''
    else:
        return ''

@register.simple_tag
def get_brs_point(student_points, student_id, checkpoint_id):
    return str(student_points[student_id][checkpoint_id])

@register.filter
def get_dict_value(dictionary, key):
    return dictionary[key] if key in dictionary.keys() else ''
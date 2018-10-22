from datetime import *
from django.db import transaction
from umo.models import EduOrg, CheckPoint, Group, BRSpoints


def check_edu_org(name, parent):
    if len(parent) > 0:
        parent = check_edu_org(parent, '')
    else:
        parent = None
    try:
        edu_org = EduOrg.objects.get(name__icontains=name)
    except Exception as e:
        edu_org = add_edu_org(name, parent)
    return edu_org


def add_edu_org(name, parent):
    edu_org = EduOrg()
    edu_org.name = name
    edu_org.uni = parent
    edu_org.save()
    return edu_org


def add_brs(course, group_list, check_points):
    if course.brspoints_set.all().exists():
        return
    with transaction.atomic():
        for student_in_list in group_list:
            for check_point in check_points:
                BRSpoints.objects.create(student=student_in_list.student, checkpoint=check_point, course=course, points=0)


def get_check_points():
    check_points = CheckPoint.objects.all()
    if not check_points:
        check_points = add_check_points()
    return check_points


def add_check_points():
    with transaction.atomic():
        CheckPoint.objects.create(name="1 контроль. срез")
        CheckPoint.objects.create(name="2 контроль. срез")
        CheckPoint.objects.create(name="Рубежный срез")
    CheckPoint.objects.all()
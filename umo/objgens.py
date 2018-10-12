from umo.models import Specialization, EduOrg, Qual, Level


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
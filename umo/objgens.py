from datetime import *
from django.db import transaction
from umo.models import EduOrg, CheckPoint, Group, BRSpoints, Exam, ExamMarks


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
    st_ids = group_list.values_list('student__id', flat=True)
    if course.brspoints_set.filter(student__id__in=st_ids).exists():
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
    return CheckPoint.objects.all()


def add_exam(course, group_list, exam_date, control_type, prev_exam=None):
    with transaction.atomic():
        exam = Exam()
        exam.course = course
        exam.examDate = exam_date
        exam.controlType = control_type
        exam.prev_exam = prev_exam
        exam.save()
        add_exam_marks(exam, group_list)
        return exam


def add_exam_marks(exam, group_list):
    checkpoint = CheckPoint.objects.get(name__icontains='Рубежный')
    for gl in group_list:
        mark = ExamMarks.objects.filter(exam__id=exam.id, student__id=gl.student.id).first()
        if mark is None:
            mark = ExamMarks()
            mark.exam = exam
            mark.student = gl.student
            mark.additional_points = 0
            mark.examPoints = 0
            mark.mark = 2
            mark.mark_symbol = ExamMarks.SYMBOL_MARK[-1][0]
        p = BRSpoints.objects.filter(course__id=exam.course.id, student__id=gl.student.id, points__gt=0).order_by(
            '-checkpoint__id').first()
        if p is not None:
            mark.inPoints = p.points
        else:
            mark.inPoints = 0
        mark.save()
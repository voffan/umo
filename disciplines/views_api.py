import datetime
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from nomenclature.form import AddSubjectToteacherForm
from umo.models import BRSpoints, CheckPoint, CourseMaxPoints, Course, Teacher, ExamMarks, Exam


def to_number(data):
    if type(data) is str:
        return float(data.replace(',','.'))
    else:
        return float(data)


@login_required
@permission_required('umo.change_brspoints', login_url='login')
def brs_scores(request):
    result = {"result":False}
    status = 200
    serialized_data = request.body.decode("utf-8")
    serialized_data = json.loads(serialized_data)
    course = Course.objects.filter(id=serialized_data['course_id']).first()
    max_points = dict(course.coursemaxpoints_set.all().values_list('checkpoint__id','max_point'))
    scores = BRSpoints.objects.select_related('student', 'course').filter(course__id=course.id, student__id=serialized_data['student_id']).order_by('checkpoint__id')
    if not scores:
        status = 404
    elif not max_points:
        status = 406
    elif request.user.id != scores[0].course.lecturer.user.id and (not request.user.groups.filter(name='UMO').exists()):
        status = 403
    elif course.is_finished:
        status = 405
    else:
        result = {
            "student_id": str(scores[0].student.id),
            "course_id": str(scores[0].course.id),
            "fullname": str(scores[0].student.FIO)
        }
        previous = float(serialized_data['checkpoint_' + str(scores.first().checkpoint.id)])
        is_ascending = True
        exceed = previous > max_points[scores.first().checkpoint.id]
        last = max([i for i, val in enumerate(scores) if float(serialized_data['checkpoint_' + str(val.checkpoint.id)]) != 0])
        for i in range(1, last + 1):
            points = float(serialized_data['checkpoint_' + str(scores[i].checkpoint.id)])
            if points < previous:
                is_ascending = False
                break
            if exceed or points > max_points[scores[i].checkpoint.id]:
                exceed = True
                break
            previous = points
        if is_ascending and not exceed:
            try:
                with transaction.atomic():
                    for score in scores:
                        score.points = serialized_data['checkpoint_' + str(score.checkpoint.id)]
                        result['checkpoint_' + str(score.checkpoint.id)] = serialized_data['checkpoint_' + str(score.checkpoint.id)]
                        score.save()
            except:
                status = 500
        elif not is_ascending:
            status = 409
        elif exceed:
            status = 411
    return HttpResponse(
        json.dumps(result),
        content_type='application/json',
        status=status
    )


@login_required
@permission_required('umo.change_brspoints', login_url='login')
def set_max_points(request):
    result = {"result": False}
    status = 200
    checkpoints = CheckPoint.objects.all()
    course = get_object_or_404(Course, pk=request.POST['course'])
    if course.is_finished:
        status = 405
    elif course.lecturer.user.id != request.user.id and (not request.user.groups.filter(name='UMO').exists()):
        status = 403
    else:
        result['data'] = {}
        try:
            with transaction.atomic():
                for checkpoint in checkpoints:
                    mpoints, created = CourseMaxPoints.objects.update_or_create(course=course, checkpoint=checkpoint, defaults={'max_point': request.POST['checkpoint_'+str(checkpoint.id)]})
                    result['data'][checkpoint.id] = mpoints.max_point
        except:
            status = 500
    return JsonResponse(
        result,
        status=status
    )


@login_required
@permission_required('umo.change_brspoints', login_url='login')
def get_max_points(request):
    result = {'result': False}
    if 'course' in request.GET:
        result['result'] = True
        result['data'] = dict(CourseMaxPoints.objects.filter(course__id=request.GET['course']).values_list('checkpoint__id', 'max_point'))
    return JsonResponse(result)


@login_required
@permission_required('umo.change_course', login_url='login')
def add_course_to_teacher(request):
    result = {'result': True}
    table_rows = ''
    form = AddSubjectToteacherForm(request.POST)
    if form.is_valid():
        try:
            with transaction.atomic():
                teacher = Teacher.objects.get(pk=form.cleaned_data['teacher'])
                for course in form.cleaned_data['courses']:
                    if course.lecturer is not None:
                        continue
                    course.lecturer = teacher
                    course.save()
                    table_rows += '<tr><td>' + course.discipline_detail.discipline.code + '</td>' + \
                                  '<td><a href="' + reverse('disciplines:detail', args=[course.id]) + '">' + course.discipline_detail.discipline.Name + '</a></td>' + \
                                  '<td>' + str(course.discipline_detail.semester) +'</td>' + \
                                  '<td>' + course.group.Name + '</td>' + \
                                  '<td>' + teacher.FIO + '</td>' + \
                                  '<td><div class="dropdown">' + \
                                      '<button class="btn btn-secondary dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Действия</button>' + \
                                      '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' + \
                                          '<a class="dropdown-item" href="' + reverse('disciplines:brs_scores', args=[course.id]) + '">Баллы БРС</a>' + \
                                          '<a class="dropdown-item" href="#" name="delete_course" id="' + str(course.id) + '">Снять привязку</a>' + \
                                      '</div>' + \
                                  '</div> </td>' + \
                                  '</tr>'
                result['rows'] = table_rows
        except Exception as e:
            result['result'] = False
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
@permission_required('umo.change_course', login_url='login')
def delete_course_teacher(requst):
    result = {'result':True}
    try:
        course = Course.objects.get(pk=requst.POST['course'])
        course.lecturer = None
        course.save()
        result['course'] = course.id
    except Exception as e:
        result['result'] = False
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
@permission_required('umo.change_exammarks', login_url='login')
def exam_scores(request):
    result = {'result': False}
    serialized_data = request.body.decode("utf-8")
    serialized_data = json.loads(serialized_data)
    score = ExamMarks.objects.filter(exam__pk=serialized_data['exam_id'],
                                     student__id=serialized_data['student_pk']).first()
    result['old'] = {'additional_points': score.additional_points, 'exam_points': score.examPoints,
                     'mark': score.mark_to_text, 'symbol': score.mark_symbol, 'total': score.total_points }
    final = CheckPoint.objects.get(name__icontains='Рубеж')
    max_in_points = CourseMaxPoints.objects.get(course__id=score.exam.course.id, checkpoint__id=final.id).max_point
    serialized_data['additional_points'] = to_number(serialized_data['additional_points'])
    serialized_data['exam_points'] = to_number(serialized_data['exam_points'])
    result['max_exam_points'] = 0

    if score is None:
        status = 404
    elif score.exam.is_finished:
        status = 405
    elif request.user.id != score.exam.course.lecturer.user.id and (not request.user.groups.filter(name='UMO').exists()):
        status = 403
    elif score.inPoints + serialized_data['exam_points'] + serialized_data['additional_points'] > 100:
        status = 400
    elif serialized_data['exam_points'] > 100 - max_in_points:
        result['max_exam_points'] = 100 - max_in_points
        status = 406
    else:
        try:
            score.additional_points = serialized_data['additional_points']
            score.examPoints = serialized_data['exam_points']
            if serialized_data['absence']:
                score.mark = 0
            elif serialized_data['individual']:
                score.mark = 1
            else:
                score.mark = 9
            score.save()
            result['new'] = {'additional_points': score.additional_points, 'exam_points': score.examPoints,
                             'mark': score.mark_to_text, 'symbol': score.mark_symbol, 'total': score.total_points ,
                             'absence': score.mark == 0, 'individual': score.mark == 1}
            result['result'] = True
            status = 200
        except Exception as e:
            status = 500
    result['status'] = status
    return JsonResponse(result, status=status)


@login_required
@permission_required('umo.change_exam', login_url='login')
def finish_exam(request):
    result = {'result': False}
    exam = Exam.objects.filter(id=request.POST['exam_id']).first()
    if exam is None:
        status = 400
    elif request.user.id != exam.course.lecturer.user.id and (not request.user.groups.filter(name='UMO').exists()):
        status = 403
    else:
        try:
            with transaction.atomic():
                exam.course.is_finished=True
                exam.course.save()
                exam.is_finished = True
                exam.save()
            result['result'] = True
            status = 200
        except Exception as e:
            status = 500
    result['status'] = status
    return JsonResponse(result, status=status)


@login_required
@permission_required('umo.change_exam', login_url='login')
def set_exam_date(request):
    date = datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d')
    exam_id = int(request.POST['exam_id'])
    exam = Exam.objects.filter(id=exam_id).first()
    result = {'result': False, 'date': exam.examDate.strftime('%Y-%m-%d')}
    status = 200
    if exam is None:
        status = 400
    elif request.user.id != exam.course.lecturer.user.id and (not request.user.groups.filter(name='UMO').exists()):
        status = 403
    elif date > datetime.datetime.now():
        status = 406
    else:
        try:
            exam.examDate = date
            exam.save()
            result['result'] = True
        except:
            status = 500
    print(result, status)
    print(request.POST)
    return JsonResponse(result, status=status)

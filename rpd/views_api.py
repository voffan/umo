import datetime
import json

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse

from rpd.models import RPDDiscipline, DisciplineResult, Basement, RPDDisciplineContentHours, RPDDisciplineContent, \
    PracticeDescription, DisciplineRating, MarkScale, FOS, Bibliography, Language
from umo.models import (Teacher, Group, GroupList, Synch, Year, EduProgram, Student, Discipline, CheckPoint, Control,
                        DisciplineDetails, BRSpoints, EduPeriod, ExamMarks, Exam, Course, Person, Competency,
                        CompetencyIndicator)

def delete_result(request):
    result = {'result': False}
    if 'result_id' in request.GET:
        result['result'] = True
        status = 200
        res = DisciplineResult.objects.filter(id=request.GET['result_id']).first()
        res.delete()

    return JsonResponse(result, status=status)

def delete_basement(request):
    result = {'result': False}
    if 'basement_id' in request.GET:
        result['result'] = True
        status = 200
        res = Basement.objects.filter(id=request.GET['basement_id']).first()
        res.delete()

    return JsonResponse(result, status=status)

def delete_theme(request):
    result = {'result': False}
    if 'theme_id' in request.GET:
        result['result'] = True
        status = 200
        res = RPDDisciplineContent.objects.filter(id=request.GET['theme_id']).first()
        res.delete()

    return JsonResponse(result, status=status)
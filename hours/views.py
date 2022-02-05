from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from umo.models import (Teacher, Group, GroupList, Synch, Year, EduProgram, Student, Discipline, CheckPoint, Control,
                        DisciplineDetails, BRSpoints, EduPeriod, ExamMarks, Exam)
from hours.models import (DisciplineSetting, GroupInfo, CourseHours, SupervisionHours, PracticeHours, OtherHours, CathedraEmployee)


class CourseList(PermissionRequiredMixin, ListView):
    permission_required = 'umo.add_course'
    template_name = 'course_list.html'
    model = CourseHours

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user__id=self.request.user.id)
        return CourseHours.objects.filter(cathedra__id=teacher.id)




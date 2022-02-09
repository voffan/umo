from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.conf import settings
import os

from umo.models import (Teacher, Group, GroupList, Synch, Year, EduProgram, Student, Discipline, CheckPoint, Control,
                        DisciplineDetails, BRSpoints, EduPeriod, ExamMarks, Exam)
from hours.models import (DisciplineSetting, GroupInfo, CourseHours, SupervisionHours, PracticeHours, OtherHours, CathedraEmployee)

from .form import UploadFileForm

from nomenclature.views import hadle_uploaded_file


class CourseList(PermissionRequiredMixin, ListView):
    permission_required = 'hours.add_course'
    template_name = 'course_list.html'
    model = CourseHours

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user__id=self.request.user.id)
        return CourseHours.objects.filter(cathedra__id=teacher.cathedra.id)


class ContingentList(PermissionRequiredMixin, ListView):
    permission_required = 'hours.add_contingent'
    template_name = 'contingent_list.html'
    model = GroupInfo

    def get_queryset(self):
        return GroupInfo.objects.all()


def upload_course(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f=hadle_uploaded_file(request.FILES['file'].name, request.FILES['file'])
            # cathedra = Teacher.objects.get(user__id=request.user.id).cathedra
            upload_courses(f)
            print ('Courses are uploaded')
            # return redirect(reverse('nomenclature:rup'))

    form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form, 'header': 'курсов'})


def upload_courses(file):
    pass


def upload_contingent(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f=hadle_uploaded_file(request.FILES['file'].name, request.FILES['file'])
            # cathedra = Teacher.objects.get(user__id=request.user.id).cathedra
            upload_contingents(f)
            print('Contingent are uploaded')
            # return redirect(reverse('nomenclature:rup'))

    form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form, 'header': 'контингента'})


def upload_contingents(file):
    pass


class ContingentUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'hours.change_contingent'
    template_name = 'contingent_edit.html'
    success_url = reverse_lazy('hours:contingent_list')
    model = GroupInfo
    fields = ['group', 'group_type', 'subgroup', 'amount']


class EmployeeList(PermissionRequiredMixin, ListView):
    permission_required = 'hours.add_employee'
    template_name = 'employee_list.html'
    model = CathedraEmployee

    def get_queryset(self):
        return CathedraEmployee.objects.all()


class EmployeeUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'hours.change_employee'
    template_name = 'employee_edit.html'
    success_url = reverse_lazy('hours:employee_list')
    model = CathedraEmployee
    fields = ['teacher', 'stavka', 'employee_type', 'is_active']





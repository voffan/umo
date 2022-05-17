from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group as auth_groups
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login, update_session_auth_hash
from django.core.validators import validate_email
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import ModelForm, CharField, ValidationError, PasswordInput, HiddenInput
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Alignment, Protection, Font, Side

import synch.models as sync_models
from umo.models import (Teacher, Group, GroupList, Synch, Year, EduProgram, Student, Discipline, CheckPoint, Control,
                        DisciplineDetails, BRSpoints, EduPeriod, ExamMarks, Exam)


def index(request):
    if auth_groups.objects.get(name='teacher') in request.user.groups.all():
        return redirect('disciplines:mysubjects')
    else:
        return redirect('disciplines:disciplines_list')

# Create your views here.
class RPD(PermissionRequiredMixin):
    permission_required = 'rpd.add_rpd'
    template_name = 'rpd.html'
    model = Teacher


# class TeacherList(PermissionRequiredMixin, ListView):
#     permission_required = 'umo.add_teacher'
#     template_name = 'teachers_list.html'
#     model = Teacher
#
#
# class TeacherCreate(PermissionRequiredMixin, CreateView):
#     permission_required = 'umo.change_teacher'
#     template_name = 'teacher_form.html'
#     success_url = reverse_lazy('teachers:list_teachers')
#     model = Teacher
#     fields = ['FIO', 'position', 'zvanie', 'cathedra', 'user']
#
#
# class TeacherUpdate(PermissionRequiredMixin, UpdateView):
#     permission_required = 'umo.change_teacher'
#     template_name = 'teacher_edit.html'
#     success_url = reverse_lazy('teachers:list_teachers')
#     model = Teacher
#     fields = ['last_name', 'first_name', 'second_name', 'position', 'title', 'cathedra']
#
#
# class TeacherDelete(PermissionRequiredMixin, DeleteView):
#     permission_required = 'umo.delete_teacher'
#     model = Teacher
#     success_url = reverse_lazy('teachers:list_teachers')
#     template_name = 'teacher_delete.html'
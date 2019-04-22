from datetime import datetime

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group as auth_groups
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

import synch.models as sync_models
from umo.models import (Teacher, Group, GroupList, Synch, Year, EduProgram, Student, Discipline, CheckPoint, Control,
                        DisciplineDetails, BRSpoints, EduPeriod, ExamMarks, Mark, Exam)


# Create your views here.

class StudentsList(PermissionRequiredMixin, ListView):
    permission_required = 'umo.view_student'
    model = GroupList
    context_object_name = 'student_list'
    success_url = reverse_lazy('students:student_changelist')
    template_name = "students_list.html"

    def get_queryset(self):
        return GroupList.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(StudentsList, self).get_context_data(**kwargs)
        synch = Synch.objects.last()
        if synch is not None:
            context['date'] = str(synch.date)
        else:
            context['date'] = 'нет'
        return context


class StudentListView(StudentsList):
    permission_required = 'umo.add_student'

    def post(self, request, *args, **kwargs):
        if (request.POST.get('synch')):
            with transaction.atomic():
                synch = Synch.objects.last()
                if synch is not None:
                    if synch.finished:
                        synch = Synch()
                        synch.finished = False
                else:
                    synch = Synch()
                    synch.finished = False
                synch.date = datetime.now()
                synch.save()
                synch = Synch.objects.last()
                synch_groups = sync_models.PlnGroupStud.objects.filter(id_pln__id_dop__id_institute=1118)
                for sg in synch_groups:
                    eduprogyear = sync_models.PlnEduProgYear.objects.filter(id_pln=sg.id_pln.id_pln).first()
                    if synch.date > eduprogyear.dateend:
                        continue

                    if Group.objects.filter(id=sg.id_group).first() is not None:
                        g = Group.objects.filter(id=sg.id_group).first()
                    else:
                        g = Group()
                        g.id = sg.id_group
                    g.begin_year = Year.objects.get_or_create(year=eduprogyear.year)[0]
                    g.Name = sg.name
                    g.program = EduProgram.objects.filter(specialization__code=eduprogyear.id_dop.id_spec.code, year__year__lte=eduprogyear.year).order_by('-year__year').first()
                    g.save()

                    synch_people = sync_models.PeoplePln.objects.filter(id_group=sg.id_group)
                    for sp in synch_people:
                        if sp.id_status != 2:
                            continue
                        if GroupList.objects.filter(id=sp.id_peoplepln).first() is not None:
                            gl = GroupList.objects.filter(id=sp.id_peoplepln).first()
                            st = gl.student
                        else:
                            gl = GroupList()
                            gl.id = sp.id_peoplepln
                            st = Student()
                            st.id = sp.id_people.id_people
                        st.FIO = sp.id_people.fio
                        st.student_id = str(sp.id_people.id_people)
                        st.save()
                        gl.student = st
                        gl.group = g
                        gl.active = True
                        gl.save()
                synch.finished = True
                synch.save()
        return redirect(self.success_url)


class StudentCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'umo.add_student'
    model = GroupList
    fields = ['group']
    success_url = reverse_lazy('student_changelist')
    template_name = "student_form.html"

    def get_context_data(self, **kwargs):
        context = super(StudentCreateView, self).get_context_data(**kwargs)
        context['title'] = "Добавление студента"
        return context

    def form_valid(self, form):
        student_ = Student.objects.create()
        student_.FIO = form.data.get('fio')
        student_.StudentID = form.data.get('studid')
        student_.save()
        grouplist_ = form.save(commit=False)
        grouplist_.student = student_
        grouplist_.active = True
        grouplist_.save()
        return super().form_valid(form)


@permission_required('umo.delete_student', login_url='/auth/login')
def student_delete(request):
    if request.method == 'POST':
        student_ = Student.objects.get(id = request.POST['item_id'])
        grouplist_ = GroupList.objects.get(student__id = student_.id)
        grouplist_.active = False
        return redirect('students:student_changelist')


class StudentUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'umo.change_student'
    model = GroupList
    fields = ['group']
    success_url = reverse_lazy('students:student_changelist')
    template_name = "student_form.html"
    context_object_name = 'student_list'

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Изменение студента"
        return context

    def form_valid(self, form):
        student_ = self.object.student
        student_.FIO = form.data.get('fio')
        student_.StudentID = form.data.get('studid')
        student_.save()
        grouplist_ = self.object
        grouplist_.student = student_
        grouplist_.active = True
        grouplist_.save()
        return super().form_valid(form)
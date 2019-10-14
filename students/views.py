from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group as auth_groups
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

import synch.models as sync_models
from umo.models import (Teacher, Group, GroupList, Synch, Year, EduProgram, Student, Discipline, CheckPoint, Control,
                        DisciplineDetails, BRSpoints, EduPeriod, ExamMarks, Mark, Exam, Course, Semester)
from students.forms import GetGroupPointsForm
from students.views_excel import export_group_points

from transliterate import translit

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
                #synch = Synch.objects.last()
                synch_groups = sync_models.PlnGroupStud.objects.filter(id_pln__id_dop__id_institute=1118, id_pln__dateend__gte=synch.date.strftime('%Y-%m-%d'))
                n = synch_groups.count()
                i = 1
                for sg in synch_groups:
                    print(i, 'of', n)
                    eduprogyear = sg.id_pln#sync_models.PlnEduProgYear.objects.filter(id_pln=sg.id_pln.id_pln).first()
                    '''if synch.date > eduprogyear.dateend:
                        continue'''

                    if Group.objects.filter(id=sg.id_group).first() is not None:
                        g = Group.objects.filter(id=sg.id_group).first()
                    else:
                        g = Group()
                        g.id = sg.id_group
                    g.begin_year = Year.objects.get_or_create(year=eduprogyear.year)[0]
                    g.Name = sg.name
                    g.program = EduProgram.objects.filter(specialization__code=eduprogyear.id_dop.id_spec.code, year__year__lte=eduprogyear.year).order_by('-year__year').first()
                    if g.program is not None:
                        g.cathedra = g.program.cathedra
                    g.save()

                    synch_people = sync_models.PeoplePln.objects.filter(id_group=sg.id_group)
                    for sp in synch_people:
                        gl = GroupList.objects.filter(id=sp.id_peoplepln).first()
                        if sp.id_status != 2:
                            if gl is not None:
                                gl.active = False
                                gl.save()
                            continue
                        if gl is not None:
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
                i += 1
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


def group_brs_points(group, semester, check_point):
    group_data = {'group': group, 'group_points': []}
    for sl in group.grouplist_set.all().order_by('student__FIO'):
        student_points = {}
        student_points['scores'] = list(BRSpoints.objects.filter(student__id=sl.student.id,
                                                                 checkpoint__id=check_point.id,
                                                                 course__discipline_detail__semester__id=semester.id).values_list('course__id', 'points'))
        student_points['fullname'] = sl.student.FIO
        group_data['group_points'].append(student_points)
    group_data['courses'] = list(Course.objects.filter(group__id=group.id,
                                                       discipline_detail__semester__id=semester.id).values_list('id', 'discipline_detail__discipline__Name'))
    return group_data


@login_required
#@permission_required('umo.delete_student', login_url='/auth/login')
def group_points(request):
    try:
        person = request.user.person_set.get()
        institute = Teacher.objects.get(pk=person.id).cathedra.institution
    except:
        return HttpResponse('You are not teacher!')
    #group = Group.objects.all()#filter(cathedra__institution__id=institute.id)
    group = Group.objects.get(pk=request.GET['group']) if 'group' in request.GET else Group.objects.filter(program__isnull=False).first()
    if group.program is None:
        return HttpResponse('Программа обучения группы не установлена')
    check_point = CheckPoint.objects.get(pk=request.GET['checkpoint']) if 'checkpoint' in request.GET else CheckPoint.objects.first()
    semester = Semester.objects.get(pk=request.GET['semester']) if 'semester' in request.GET else Semester.objects.get(name=group.current_semester)
    if 'excel' in request.GET:
        wb = export_group_points(group, semester)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=' + translit(group.Name, 'ru', reversed=True) + '_sem_' + semester.name + '.xlsx'
        wb.save(response)
        return response
    else:
        group_points_data = group_brs_points(group, semester, check_point)
        form = GetGroupPointsForm(initial={'group':group.id, 'semester': semester.id, 'checkpoint': check_point.id})
        return render(request,'group_points.html', {'data':group_points_data, 'form': form})
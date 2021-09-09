from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group as auth_groups, User
from django.db import transaction
from django.db.models import OuterRef, Subquery
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import ModelForm, CharField, ValidationError, PasswordInput, HiddenInput, IntegerField, TextInput
from django.contrib.auth.password_validation import validate_password
from django.core.validators import validate_email
from django.contrib.auth import login, update_session_auth_hash
from django.utils.crypto import get_random_string

import synch.models as sync_models
from umo.models import (Teacher, Group, GroupList, Synch, Year, EduProgram, Student, Discipline, CheckPoint, Control,
                        DisciplineDetails, BRSpoints, EduPeriod, ExamMarks, Exam, Course, Semester)
from students.forms import GetGroupPointsForm, GiveLoginAndPassForm
from students.views_excel import export_group_points, export_exam_points, group_access_data

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
                #ИТИ - 1129
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
                        edu_program = EduProgram.objects.filter(specialization__code=eduprogyear.id_dop.id_spec.code,
                                                                year__year__lte=eduprogyear.year).order_by(
                                                                '-year__year').first()
                        g.program = edu_program
                        if edu_program is not None:
                            g.cathedra = edu_program.cathedra
                    g.begin_year = Year.objects.get_or_create(year=eduprogyear.year)[0]
                    g.Name = sg.name
                    g.save()

                    synch_people = sync_models.PeoplePln.objects.filter(id_group=sg.id_group)
                    for sp in synch_people:
                        gl = GroupList.objects.filter(id=sp.id_peoplepln).first()
                        if sp.id_status != 2 and sp.id_status != 6 and sp.id_status != 9:
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
                        st.save()
                        gl.student = st
                        gl.group = g
                        gl.active = True
                        gl.save()
                    i += 1
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


def group_brs_points(group, semester, check_point):
    group_data = {'group': group, 'group_points': [], 'semester': semester.name}
    students = Student.objects.filter(grouplist__group__id=group.id, grouplist__active=True).order_by('FIO')
    for sl in students:
        student_points = {}
        student_points['scores'] = list(BRSpoints.objects.filter(student__id=sl.id,
                                                                 checkpoint__id=check_point.id,
                                                                 course__discipline_detail__semester__id=semester.id).values_list('course__id', 'points'))
        student_points['fullname'] = sl.FIO
        group_data['group_points'].append(student_points)
    group_data['courses'] = list(Course.objects.filter(group__id=group.id,
                                                       discipline_detail__semester__id=semester.id).values_list('id', 'discipline_detail__discipline__Name'))
    return group_data


def group_exam_results(group, semester):
    MARKS = ["Неявка", "Инд.п.", "Неуд.", "Удовл.", "Хор.", "Отл.", "Зач.", "Не зач.", "Не атт.", ""]
    group_data = {'group': group, 'group_points': [], 'semester': semester.name}
    students = Student.objects.filter(grouplist__group__id=group.id, grouplist__active=True).order_by('FIO')
    group_data['courses'] = list(Course.objects.filter(group__id=group.id,
                                                       discipline_detail__semester__id=semester.id).
                                 values_list('id', 'discipline_detail__discipline__Name'))
    for sl in students:
        student_points = dict()
        student_points['scores'] = list(ExamMarks.objects.filter(student__id=sl.id,
                                                                 exam__course__discipline_detail__semester__id=semester.id).
                                        values_list('exam__course__id', 'mark'))
        for i in range(len(student_points['scores'])):
            student_points['scores'][i] = (student_points['scores'][i][0], MARKS[student_points['scores'][i][1]])
        student_points['fullname'] = sl.FIO
        group_data['group_points'].append(student_points)
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
    is_exam = 'exam' in request.GET
    group_points_data = group_exam_results(group, semester) if is_exam else group_brs_points(group, semester, check_point)
    if 'excel' in request.GET:
        wb = export_exam_points(group_points_data) if is_exam else export_group_points(group, semester)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=' + translit(group.Name, 'ru', reversed=True) + '_sem_' + semester.name + '.xlsx'
        wb.save(response)
        return response
    else:
        form = GetGroupPointsForm(initial={'group':group.id, 'semester': semester.id, 'checkpoint': check_point.id, 'exam': is_exam})
        return render(request,'group_points.html', {'data':group_points_data, 'form': form, 'is_exam': is_exam})


@login_required
@permission_required('umo.view_course', login_url='/auth/login')
def subjects(request):
    try:
        student = Student.objects.get(user__id=request.user.id)
        group = Group.objects.get(grouplist__student__id=student.id)
        brspoints1 = BRSpoints.objects.filter(course__id=OuterRef('pk'),
                                              checkpoint__name='1 контроль. срез',
                                              student__id=student.id)
        brspoints2 = BRSpoints.objects.filter(course__id=OuterRef('pk'),
                                              checkpoint__name='2 контроль. срез',
                                              student__id=student.id)
        brspoints3 = BRSpoints.objects.filter(course__id=OuterRef('pk'),
                                              checkpoint__name='Рубежный срез',
                                              student__id=student.id)
        exam_mark = ExamMarks.objects.filter(exam__course__id=OuterRef('pk'), student__id=student.id).order_by('-exam__examDate')[:1]

        disciplines = group.course_set.select_related('discipline_detail').all().annotate(points1=Subquery(brspoints1.values('points')),
                                                                                          points2=Subquery(brspoints2.values('points')),
                                                                                          points3=Subquery(brspoints3.values('points')),
                                                                                          mark=Subquery(exam_mark.values('mark')))
        form = None
        print(disciplines)
    except:
        return render(request, 'disc_error.html')
    return render(request, 'disc_list_student.html', {'discipline_list': disciplines, 'form': form,
                                                      'student': student, 'group': group, 'exam_marks': dict(ExamMarks.MARKS)})


class StudentProfileForm(ModelForm):
    student_id = IntegerField(label='Номер зачетной книжки', required=False, widget=TextInput)
    email = CharField(max_length=50, label='Email', required=True)
    current_password = CharField(max_length=100, label='Текущий пароль', required=False, widget=PasswordInput)
    password = CharField(max_length=100, label='Пароль', required=False, widget=PasswordInput)
    confirmation = CharField(max_length=100, label='Подтверждение пароля', required=False, widget=PasswordInput)

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['student_id'].widget.attrs['readonly'] = True

    class Meta:
        model = Student
        fields = ['last_name', 'first_name', 'second_name']
        #widgets = {'id': HiddenInput()}

    def clean(self):
        #cleaned_data = super.clean()
        validate_email(self.cleaned_data['email'])
        crnt_pwd = self.cleaned_data['current_password']
        pwd = self.cleaned_data['password']
        confirmation = self.cleaned_data['confirmation']
        if pwd != confirmation:
            raise ValidationError('Введенные пароли не совпадают!')
        if pwd != '':
            if not self.instance.user.check_password(crnt_pwd):
                raise ValidationError('Текущий пароль неверен!')
            validate_password(pwd)
        return self.cleaned_data

    def save(self, commit=True):
        with transaction.atomic():
            student = super(StudentProfileForm, self).save(commit=False)
            student.FIO = self.cleaned_data['last_name'] + ' ' + self.cleaned_data['first_name'] + ' ' + self.cleaned_data['second_name']
            student.save()
            user = student.user
            if self.cleaned_data['email'] != self.instance.user.email:
                user.email = self.cleaned_data['email']
            if user is not None and self.cleaned_data['password'] != '':
                user.set_password(self.cleaned_data['password'])
            user.save()
            return student


@login_required
@permission_required('umo.change_student', login_url='/auth/login')
def student_profile(request):
    student = Student.objects.filter(user__id=request.user.id).first()
    success_message = None
    if student is not None:
        if request.method == 'POST':
            temp_post = request.POST.copy()
            temp_post['student_id'] = student.student_id
            request.POST = temp_post
            form = StudentProfileForm(request.POST, instance=student)
            if form.is_valid():
                try:
                    form.save()
                    update_session_auth_hash(request, student.user)
                    success_message = 'Профиль успешно сохранен!!'
                except:
                    form.add_error('first_name', 'Ошибка сохранения данных!')
        else:
            form = StudentProfileForm(instance=student, initial={'email': request.user.email, 'student_id': student.student_id})
        return render(request, 'student_edit.html', {'form': form, 'success_message': success_message, 'profile': 1})
    return HttpResponse('Ошибка!')


@login_required
@permission_required('umo.view_student', login_url='/auth/login')
def group_list(request, pk):
    try:
        group = Group.objects.get(id=pk)
        students = group.grouplist_set.select_related('student').all()
    except:
        return HttpResponse('Error')
    return render(request, 'group_list.html', {'student_list': students, 'group': group})


@login_required
@permission_required('umo.change_student', login_url='/auth/login')
def give_access_student(request, pk):
    student = Student.objects.get(id=pk)
    group = Group.objects.get(grouplist__student__id=student.id)
    if request.method == 'POST':
        form = GiveLoginAndPassForm(request.POST)
        if form.is_valid():
            save_access_data(student, form.cleaned_data['login'], form.cleaned_data['password'])
            return HttpResponseRedirect(reverse('students:group_list', kwargs={'pk':group.id}))
    else:
        form = GiveLoginAndPassForm()
    return render(request, 'student_access_data.html', {'student': student, 'form': form, 'group': group})


@transaction.atomic
def save_access_data(student, s_login, s_password):
    if student.user:
        u = student.user
        u.username = s_login
        u.set_password(s_password)
        u.save()
    else:
        try:
            u = User.objects.create_user(username=s_login, password=s_password)
            student.user = u
            student.save()
            g = auth_groups.objects.get(name='student')
            g.user_set.add(u)
            g.save()
        except Exception as e:
            print(e)
    return True


def give_access_group(group_id):
    group = Group.objects.get(id=group_id)
    group_list = group.grouplist_set.select_related('student').filter(active=True)
    dicts = []
    for g in group_list:
        s = g.student
        try:
            unique_login = translit(s.first_name[0].lower(), "ru", reversed=True) + \
                           translit(s.second_name[0].lower(), "ru", reversed=True) + '.' + \
                           translit(s.last_name.lower().replace('ь',''), "ru", reversed=True)
        except Exception as e:
            str = s.FIO
            lst = str.split()
            unique_login = translit(lst[1][0].lower(), "ru", reversed=True) + \
                           translit(lst[2][0].lower(), "ru", reversed=True) + '.' + \
                           translit(lst[0].lower(), "ru", reversed=True)
        unique_pass = get_random_string(length=16)
        try:
            save_access_data(s, unique_login, unique_pass)
            dicts.append(dict({'FIO': s.FIO, 'login': unique_login, 'password': unique_pass}))
        except Exception as e:
            dicts.append(dict({'FIO': s.FIO, 'login': '', 'password': ''}))
    return dicts


@login_required
@permission_required('umo.change_student', login_url='/auth/login')
def group_access_excel(request, pk):
    group = Group.objects.get(id=pk)
    dicts = give_access_group(pk)
    wb = group_access_data(dicts)
    if wb is not None:
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=' + translit(group.Name, 'ru',
                                                                             reversed=True) + '_access.xlsx'
        wb.save(response)
    else:
        response = HttpResponse()
        response.status_code = 404
        response.write('<p>Ошибка при формировании отчета!!</p>')
    return response
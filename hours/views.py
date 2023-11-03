import datetime
import html
import io
import zipfile

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models.functions import Cast, Concat
from django.db.models import F, CharField, Value, OuterRef, Subquery, IntegerField
import json
from django.http import HttpResponse, JsonResponse, FileResponse
from transliterate import translit
from hours.import_data import import_students, import_course, add_supervision_hours, add_practice_hours, add_other_hours
from umo.models import (Teacher, EduPeriod, Kafedra)
from hours.models import (DisciplineSetting, GroupInfo, CourseHours, SupervisionHours, PracticeHours, OtherHours,
                          CathedraEmployee, NormControl, StudentsGroup)
from .form import UploadFileForm
from nomenclature.views import hadle_uploaded_file
from hours.export_data import export_form
from zipfile import ZipFile
from io import BytesIO
from urllib.parse import urlparse, parse_qs
from django.utils.safestring import mark_safe
from django.utils.html import escape


class CourseList(PermissionRequiredMixin, ListView):
    permission_required = 'hours.add_course'
    template_name = 'course_list.html'
    model = CourseHours

    def get_queryset(self):
        teacher = get_object_or_404(Teacher, user__id=self.request.user.id)
        return CourseHours.objects.filter(cathedra__id=teacher.cathedra.id)

    def get_context_data(self, **kwargs):
        context = super(CourseList, self).get_context_data(**kwargs)
        result = []
        teacher_status = []
        for item in Teacher.objects.all():
            result.append({'id': item.id, 'FIO': item.FIO})
            teacher_status.append([item.id, int(norm_hours(item.id) and norm_stavka(item.id))])
        cathedra = []
        for item in Kafedra.objects.all():
            cathedra.append({'id': item.id, 'name': item.name})
        context['teacher'] = result
        context['teacher_status'] = teacher_status
        context['cathedra'] = cathedra

        return context


class ContingentList(PermissionRequiredMixin, ListView):
    permission_required = 'hours.add_contingent'
    template_name = 'contingent_list.html'
    model = GroupInfo

    def get_queryset(self):
        return GroupInfo.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group_type'] = GroupInfo.GROUP_TYPE
        return context


def upload_course(request):
    content = "курсы"
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = hadle_uploaded_file(request.FILES['file'].name, request.FILES['file'])
            import_course(f)
            print('Courses are uploaded')

    form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form, 'header': 'курсов', 'content': content})


def upload_contingent(request):
    content = "контингент"
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f = hadle_uploaded_file(request.FILES['file'].name, request.FILES['file'])
            import_students(f)
            print('Contingent are uploaded')

    form = UploadFileForm()
    return render(request, 'upload_file.html', {'form': form, 'header': 'контингента', 'content': content})


class ContingentUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'hours.change_contingent'
    template_name = 'contingent_edit.html'
    success_url = reverse_lazy('hours:contingent_list')
    model = GroupInfo
    fields = ['group', 'group_type', 'subgroup', 'amount']


class ContingentDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'hours.delete_contingent'
    model = GroupInfo
    success_url = reverse_lazy('hours:contingent_list')
    template_name = 'contingent_delete.html'


class EmployeeList(PermissionRequiredMixin, ListView):
    permission_required = 'hours.add_employee'
    template_name = 'employee_list.html'
    model = CathedraEmployee

    def get_queryset(self):
        return CathedraEmployee.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super(EmployeeList, self).get_context_data(**kwargs)
        teacher = []
        for item in Teacher.objects.all():
            teacher.append({'id': item.id, 'FIO': item.FIO})
        context['teacher'] = teacher
        context['employee_type'] = CathedraEmployee.STAFF_TYPE

        return context


class EmployeeCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'hours.add_employee'
    template_name = 'employee_form.html'
    success_url = reverse_lazy('hours:employee_list')
    model = CathedraEmployee
    fields = ['teacher', 'stavka', 'employee_type', 'is_active']


class EmployeeUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'hours.change_employee'
    template_name = 'employee_edit.html'
    success_url = reverse_lazy('hours:employee_list')
    model = CathedraEmployee
    fields = ['teacher', 'stavka', 'employee_type', 'is_active']


class SupervisionHoursList(PermissionRequiredMixin, ListView):
    permission_required = 'hours.add_supervision_hours'
    template_name = 'supervisionhours.html'
    model = SupervisionHours

    def get_queryset(self):
        return SupervisionHours.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['supervision_type'] = SupervisionHours.SUPERVISION_TYPE
        cathedra = []
        for item in Kafedra.objects.all():
            cathedra.append({'id': item.id, 'name': item.name})
        context['cathedra'] = cathedra
        return context


class SupervisionUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'hours.change_supervision'
    template_name = 'supervision_edit.html'
    success_url = reverse_lazy('hours:supervision_hours')
    model = SupervisionHours
    fields = ['teacher', 'group', 'students', 'supervision_type', 'hours', 'edu_period', 'cathedra']


@login_required
def get_courselist(request):
    fields_names = [f.name for f in CourseHours._meta.get_fields()]
    fields_names.extend(['subgroup', 'edu', 'intern', 'graduate', 'teaching', 'supervision_vkr', 'supervision_kp_kr',
                         'supervision_mag', 'supervision_asp', 'supervision_prog_mag', 'gek',
                         'vkr_rev', 'admis', 'ref_rev', 'is_lecture_seperate', 'practice_weekly', 'is_hourly',
                         'is_KR_KP_VKR', 'is_new', 'need_new_RPD', 'need_upd_RPD'])
    subgroup = GroupInfo.objects.filter(pk=OuterRef('group_id'))
    edu = PracticeHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'),
                                       practice_type=1)
    intern = PracticeHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'),
                                          practice_type=2)
    graduate = PracticeHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'),
                                            practice_type=3)
    teaching = PracticeHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'),
                                            practice_type=4)
    supervision_vkr = SupervisionHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'),
                                                      supervision_type=1)
    supervision_kp_kr = SupervisionHours.objects.filter(teacher_id=OuterRef('teacher_id'),
                                                        group_id=OuterRef('group_id'), supervision_type=2)
    supervision_mag = SupervisionHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'),
                                                      supervision_type=3)
    supervision_asp = SupervisionHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'),
                                                      supervision_type=4)
    supervision_prog_mag = SupervisionHours.objects.filter(teacher_id=OuterRef('teacher_id'),
                                                           group_id=OuterRef('group_id'), supervision_type=5)
    gek = OtherHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'), other_type=1)
    vkr_rev = OtherHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'), other_type=2)
    admis = OtherHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'), other_type=3)
    ref_rev = OtherHours.objects.filter(teacher_id=OuterRef('teacher_id'), group_id=OuterRef('group_id'), other_type=4)
    is_lecture_seperate = DisciplineSetting.objects.filter(pk=OuterRef('discipline_settings_id'))
    practice_weekly = DisciplineSetting.objects.filter(pk=OuterRef('discipline_settings_id'))
    is_hourly = DisciplineSetting.objects.filter(pk=OuterRef('discipline_settings_id'))
    is_KR_KP_VKR = DisciplineSetting.objects.filter(pk=OuterRef('discipline_settings_id'))
    is_new = DisciplineSetting.objects.filter(pk=OuterRef('discipline_settings_id'))
    need_new_RPD = DisciplineSetting.objects.filter(pk=OuterRef('discipline_settings_id'))
    need_upd_RPD = DisciplineSetting.objects.filter(pk=OuterRef('discipline_settings_id'))
    result = [dict(zip(fields_names, row)) for row in CourseHours.objects.select_related('edu_period').annotate(
        ep=Concat(Cast(F('edu_period__begin_year__year'), CharField()),
                  Value('-'),
                  Cast(F('edu_period__end_year__year'), CharField()))
    ).annotate(subgroup=Subquery(subgroup.values('subgroup')),
               edu=Subquery(edu.values('hours')),
               intern=Subquery(intern.values('hours')),
               graduate=Subquery(graduate.values('hours')),
               teaching=Subquery(teaching.values('hours')),
               supervision_vkr=Subquery(supervision_vkr.values('hours')),
               supervision_kp_kr=Subquery(supervision_kp_kr.values('hours')),
               supervision_mag=Subquery(supervision_mag.values('hours')),
               supervision_asp=Subquery(supervision_asp.values('hours')),
               supervision_prog_mag=Subquery(supervision_prog_mag.values('hours')),
               gek=Subquery(gek.values('hours')),
               vkr_rev=Subquery(vkr_rev.values('hours')),
               admis=Subquery(admis.values('hours')),
               ref_rev=Subquery(ref_rev.values('hours')),
               is_lecture_seperate=Subquery(is_lecture_seperate.values('is_lecture_seperate')),
               practice_weekly=Cast(Subquery(practice_weekly.values('practice_weekly')), CharField()),
               is_hourly=Subquery(is_hourly.values('is_hourly')),
               is_KR_KP_VKR=Subquery(is_KR_KP_VKR.values('is_KR_KP_VKR')),
               is_new=Subquery(is_new.values('is_new')),
               need_new_RPD=Subquery(need_new_RPD.values('need_new_RPD')),
               need_upd_RPD=Subquery(need_upd_RPD.values('need_upd_RPD')),
               ).values_list('id', 'ep', 'teacher__id', 'group__group__Name', 'cathedra__id',
                             'discipline_settings__discipline__Name', 'f_lecture', 'f_practice', 'f_lab',
                             'f_consult_hours', 'f_exam_hours', 'f_control_hours', 'f_check_hours',
                             'f_control_SRS', 'f_control_BRS', 'subgroup', 'edu', 'intern', 'graduate', 'teaching',
                             'supervision_vkr', 'supervision_kp_kr', 'gek', 'supervision_mag', 'supervision_asp',
                             'supervision_prog_mag', 'vkr_rev', 'admis', 'ref_rev', 'is_lecture_seperate',
                             'practice_weekly', 'is_hourly', 'is_KR_KP_VKR', 'is_new', 'need_new_RPD', 'need_upd_RPD')]
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
def get_contingentlist(request):
    fields_names = [f.name for f in GroupInfo._meta.get_fields() if f.concrete == True]
    fields_names.extend(['rf', 'rsa', 'd'])
    rf = StudentsGroup.objects.filter(group_id=OuterRef('id'), budget_type=0)
    rsa = StudentsGroup.objects.filter(group_id=OuterRef('id'), budget_type=1)
    d = StudentsGroup.objects.filter(group_id=OuterRef('id'), budget_type=2)
    queryset = GroupInfo.objects.annotate(rf=Subquery(rf.values('amount')),
                                          rsa=Subquery(rsa.values('amount')),
                                          d=Subquery(d.values('amount')))
    result = [dict(zip(fields_names, row)) for row in
              queryset.values_list('id', 'group__Name', 'group_type',
                                   'subgroup', 'amount', 'edu_type',
                                   'rf', 'rsa', 'd')]
    print(queryset.query)

    for item in result:
        item['group'] = '<a href="' + reverse('hours:edit_contingent', kwargs={'pk': item['id']}) + '">' + item[
            'group'] + '</a>'
        item['buttons'] = '<a href="' + reverse('hours:delete_contingent', kwargs={
            'pk': item['id']}) + '" class="btn btn-danger" style="color: white">' + 'Удалить' + '</button>'
    return HttpResponse(json.dumps(result), content_type='application/json')


def get_employeelist(request):
    fields_names = [f.name for f in CathedraEmployee._meta.get_fields() if f.concrete == True]
    fields_names.append('position')
    fields_names.append('title')
    fields_names.append('teacher_id')
    result = [dict(zip(fields_names, row)) for row in
              CathedraEmployee.objects.values_list('id', 'teacher__FIO', 'stavka', 'employee_type', 'is_active',
                                                   'teacher__position__name', 'teacher__title', 'teacher__id')]

    for item in result:
        item['teacher'] = '<a href="' + reverse('hours:edit_employee', kwargs={'pk': item['id']}) + '">' + item[
            'teacher'] + '</a>'
        # item['buttons'] = '<a href="' + reverse('hours:export_kup', kwargs={
        #     'pk': item['teacherid']}) + '" class="btn btn-danger" style="color: white">' + 'КУП' + '</button>'
    return HttpResponse(json.dumps(result), content_type='application/json')


def get_supervision_hours(request):
    fields_names = [f.name for f in SupervisionHours._meta.get_fields() if f.concrete == True]
    result = [dict(zip(fields_names, row)) for row in
              SupervisionHours.objects.select_related('edu_period').annotate(
                  ep=Concat(Cast(F('edu_period__begin_year__year'), CharField()),
                            Value('-'),
                            Cast(F('edu_period__end_year__year'), CharField())),
              ).values_list('id', 'teacher__FIO', 'group__group__Name', 'students', 'supervision_type', 'hours', 'ep',
                            'cathedra__id')]

    for item in result:
        item['teacher'] = '<a href="' + reverse('hours:edit_supervision', kwargs={'pk': item['id']}) + '">' + item[
            'teacher'] + '</a>'
    return HttpResponse(json.dumps(result), content_type='application/json')


def save_courselist(request):
    result = {'result': False, 'valid': {}}
    if request.method == 'POST':
        try:
            serialized_data = request.body.decode("utf-8")
            serialized_data = json.loads(serialized_data)
            for item in serialized_data['data']:
                course = CourseHours.objects.get(id=item[0])
                try:
                    t = Teacher.objects.get(id=int(item[2]))
                    if t is not None:
                        course.teacher = t
                except:
                    course.teacher = None
                k = Kafedra.objects.get(id=item[4])
                course.cathedra = k
                course.f_lecture = item[6]
                course.f_practice = course.discipline_settings.Practice * course.group.subgroup
                course.f_lab = item[8]
                course.f_consult_hours = item[9]
                course.f_exam_hours = item[10]
                course.f_control_hours = item[11]
                course.f_check_hours = item[12]
                course.f_control_SRS = item[13]
                course.f_control_BRS = item[14]
                ds = DisciplineSetting.objects.get(pk=course.discipline_settings.id)
                ds.is_lecture_seperate = item[23]
                ds.practice_weekly = item[24]
                ds.is_hourly = item[25]
                ds.is_kp_kr = item[26]
                ds.is_new = item[27]
                ds.need_new_rpd = item[28]
                ds.need_upd_rpd = item[29]
                ds.save()
                course.save()
                if course.teacher is not None:
                    add_supervision_hours(t, course.group, k, 1,
                                          SupervisionHours.objects.filter(teacher_id=course.teacher,
                                                                          group_id=course.group,
                                                                          edu_period_id=course.edu_period.id,
                                                                          supervision_type=1).first())
                    add_supervision_hours(t, course.group, k, 2,
                                          SupervisionHours.objects.filter(teacher_id=course.teacher,
                                                                          group_id=course.group,
                                                                          edu_period_id=course.edu_period.id,
                                                                          supervision_type=2).first())
                    add_supervision_hours(t, course.group, k, 3,
                                          SupervisionHours.objects.filter(teacher_id=course.teacher,
                                                                          group_id=course.group,
                                                                          edu_period_id=course.edu_period.id,
                                                                          supervision_type=3).first())
                    add_supervision_hours(t, course.group, k, 4,
                                          SupervisionHours.objects.filter(teacher_id=course.teacher,
                                                                          group_id=course.group,
                                                                          edu_period_id=course.edu_period.id,
                                                                          supervision_type=4).first())
                    add_supervision_hours(t, course.group, k, 5,
                                          SupervisionHours.objects.filter(teacher_id=course.teacher,
                                                                          group_id=course.group,
                                                                          edu_period_id=course.edu_period.id,
                                                                          supervision_type=5).first())
                    add_practice_hours(t, course.group, k, 1,
                                       PracticeHours.objects.filter(teacher_id=course.teacher, group_id=course.group,
                                                                    edu_period_id=course.edu_period.id,
                                                                    practice_type=1).first())
                    add_practice_hours(t, course.group, k, 2,
                                       PracticeHours.objects.filter(teacher_id=course.teacher, group_id=course.group,
                                                                    edu_period_id=course.edu_period.id,
                                                                    practice_type=2).first())
                    add_practice_hours(t, course.group, k, 3,
                                       PracticeHours.objects.filter(teacher_id=course.teacher, group_id=course.group,
                                                                    edu_period_id=course.edu_period.id,
                                                                    practice_type=3).first())
                    add_practice_hours(t, course.group, k, 4,
                                       PracticeHours.objects.filter(teacher_id=course.teacher, group_id=course.group,
                                                                    edu_period_id=course.edu_period.id,
                                                                    practice_type=4).first())
                    add_other_hours(t, course.group, k, 1,
                                    OtherHours.objects.filter(teacher_id=course.teacher, group_id=course.group,
                                                              edu_period_id=course.edu_period.id, other_type=1).first())
                    add_other_hours(t, course.group, k, 2,
                                    OtherHours.objects.filter(teacher_id=course.teacher, group_id=course.group,
                                                              edu_period_id=course.edu_period.id, other_type=2).first())
                    add_other_hours(t, course.group, k, 3,
                                    OtherHours.objects.filter(teacher_id=course.teacher, group_id=course.group,
                                                              edu_period_id=course.edu_period.id, other_type=3).first())
                    add_other_hours(t, course.group, k, 4,
                                    OtherHours.objects.filter(teacher_id=course.teacher, group_id=course.group,
                                                              edu_period_id=course.edu_period.id, other_type=4).first())
                if course.discipline_settings.is_lecture_seperate:
                    check = CourseHours.objects.filter(group_id=course.group.id, cathedra_id=course.cathedra.id,
                                                       edu_period_id=course.edu_period.id)
                    if check.count() < 2:
                        c = CourseHours()
                        c.edu_period = course.edu_period
                        c.teacher = None
                        c.group = course.group
                        c.cathedra = course.cathedra
                        ds = course.discipline_settings
                        c.discipline_settings = ds
                        c.f_lecture = course.discipline_settings.Lecture
                        course.f_lecture = 0
                        c.f_practice = course.discipline_settings.Practice
                        course.f_practice = 0
                        c.f_lab = 0
                        c.f_consult_hours = course.f_consult_hours
                        c.f_exam_hours = course.f_exam_hours
                        c.f_control_hours = course.f_control_hours
                        c.f_check_hours = 0
                        c.f_control_SRS = 0
                        c.f_control_BRS = 0
                        ds.is_lecture_seperate = False
                        ds.save()
                        c.save()
                result['valid'][t.id] = int(norm_hours(t.id) and norm_stavka(t.id))
            result['result'] = True
        except Exception as e:
            result['error'] = 'Ошибка в сохранении'
    return JsonResponse(result)


def norm_hours(teacher_id):
    norm_control = NormControl.objects.all().first().max_hours
    employee = CathedraEmployee.objects.filter(teacher__id=teacher_id).first()
    if employee is None:
        return True
    stavka = employee.stavka
    ep = EduPeriod.objects.get(active=True)
    total = 0
    for row in CourseHours.objects.filter(teacher__id=teacher_id, edu_period__id=ep.id):
        total += row.f_lecture + row.f_lab + row.f_practice + row.f_consult_hours
    if total <= stavka * float(norm_control):
        return True
    else:
        return False


def norm_stavka(teacher_id):
    norm_control = NormControl.objects.all().first().max_stavka
    employee = CathedraEmployee.objects.filter(teacher__id=teacher_id).first()
    if employee is None:
        return True
    stavka = employee.stavka
    if stavka <= float(norm_control):
        return True
    else:
        return False


def save_contingent(request):
    result = {'result': False}
    if request.method == 'POST':
        try:
            serialized_data = request.body.decode("utf-8")
            serialized_data = json.loads(serialized_data)
            for item in serialized_data['data']:
                contingent = GroupInfo.objects.get(id=item[0])
                contingent.group_type = item[2]
                contingent.subgroup = item[3]
                contingent.amount = item[4]
                contingent.save()
            result['result'] = True
        except:
            result['error'] = 'Ошибка в сохранении'
    return JsonResponse(result)


def save_employeelist(request):
    result = {'result': False}
    if request.method == 'POST':
        try:
            serialized_data = request.body.decode("utf-8")
            serialized_data = json.loads(serialized_data)
            for item in serialized_data['data']:
                print(item)
                e = CathedraEmployee.objects.get(id=item[0])
                e.stavka = item[2]
                e.employee_type = item[3]
                e.is_active = item[4]
                e.save()
            result['result'] = True
        except:
            result['error'] = 'Ошибка в сохранении'
    return JsonResponse(result)


def save_supervision_hours(request):
    result = {'result': False}
    if request.method == 'POST':
        try:
            serialized_data = request.body.decode("utf-8")
            serialized_data = json.loads(serialized_data)
            for item in serialized_data['data']:
                print(item)
                supervision = SupervisionHours.objects.get(id=item[0])
                supervision.students = item[3]
                supervision.supervision_type = item[4]
                supervision.hours = item[5]
                k = Kafedra.objects.get(id=item[7])
                supervision.cathedra = k
                supervision.save()
            result['result'] = True
        except:
            result['error'] = 'Ошибка в сохранении'
    return JsonResponse(result)


@csrf_exempt
def export_kup(request):
    teacher_ids = request.GET.getlist('ids')
    print('Teacher IDs from URL:', teacher_ids)
    excel_files = []
    for teacher_id in teacher_ids:
        teacher = get_object_or_404(Teacher, id=teacher_id)
        wb = export_form(teacher)
        excel_files.append(wb.title + '.xslx')
        wb.save(wb.title + '.xslx')
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        for excel_file in excel_files:
            zip_file.write(excel_file)

    zip_buffer.seek(0)

    export_date = str(datetime.datetime.now().strftime('%m-%d-%y %H:%M:%S'))
    response = FileResponse(zip_buffer, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename =' + export_date + '.zip'
    return response

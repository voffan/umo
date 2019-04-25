from django.db import transaction
from django.shortcuts import render, redirect
import os
import json

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.views.generic import ListView

from umo.models import Discipline, DisciplineDetails, Semester, Teacher, Specialization, Profile, Control, EduProgram, Course, Group
from .form import UploadFileForm
from .parseRUP import parseRUP
from students.forms import SetProgramToGroupsForm


#from somewhere import handle_uploaded_file

# Create your views here.

@permission_required('umo.add_discipline', login_url='/auth/login')
def subjects_save(request):
    subjects = request.POST.getlist('disc_id')
    teachers = request.POST.getlist('teachers')
    for i in range(0, len(subjects)):
        subj = Discipline.objects.get(pk=subjects[i])
        subj.lecturer = Teacher.objects.get(pk=teachers[i])
        subj.save()

    return redirect('nomenclatures:select_semester')


@permission_required('umo.add_discipline', login_url='/auth/login')
def vuborka(request):
    try:
        semester_id = request.GET['semester']
        specialization_id = request.GET['specialization']
        profile_id = request.GET['profile']
    except:
        return redirect('nomenclatures:select_semester')

    semester = Semester.objects.get(pk=semester_id)
    specialization = Specialization.objects.get(pk=specialization_id)
    profile = Profile.objects.get(pk=profile_id)

    disc_filtered = DisciplineDetails.objects.filter(semester=semester, subject__program__specialization=specialization, subject__program__profile=profile)
    teachers = Teacher.objects.all()
    disc_filtered  = DisciplineDetails.objects.filter(semester=semester, subject__program__specialization=specialization, subject__program__profile=profile)
    teachers = Teacher.objects.all().order_by('FIO')

    return render(request, 'select_teacher.html', {'disciplines': disc_filtered, 'teachers':teachers})


@permission_required('umo.add_discipline', login_url='/auth/login')
def select_semester(request):
    semester_list = Semester.objects.all().order_by('name')
    specialization_list = Specialization.objects.all().order_by('name')
    profile_list = Profile.objects.all().order_by('name')
    return render(request, 'select_semester.html', {'semesters':semester_list, 'specializations':specialization_list, 'profiles':profile_list})


def nomenclature_discipline(request):
    courses = Course.objects.select_related('discipline_detail', 'lecturer', 'group').all().order_by('discipline_detail__semester')
    teachers = Teacher.objects.all().order_by('FIO')
    control = Control.objects.all().order_by('control_type')

    return render(request, 'nomenclature_disciplines.html', {'courses':courses, 'teachers':teachers, 'controls':control})


@permission_required('umo.add_discipline', login_url='/auth/login')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #save_path = os.path.join(settings.MEDIA_ROOT, 'upload', request.FILES['filename'].name)
            #path = default_storage.save(save_path, request.FILES['file'])
            #return default_storage.path(path)
            f=hadle_uploaded_file(request.FILES['file'].name, request.FILES['file'])
            parseRUP(f)
            return redirect(reverse('nomenclature:rup'))

    else:
        form = UploadFileForm()
    return render(request, 'rup_upload.html', {'form': form})


#@permission_required('umo.add_discipline', login_url='/auth/login')
def hadle_uploaded_file(filename, file):
     s=os.path.join(settings.BASE_DIR, 'upload',  filename)
     with open(s, 'wb+') as destination:
         for chunk in file.chunks():
             destination.write(chunk)
     return s


class EduProgListView(PermissionRequiredMixin, ListView):
    permission_required = 'umo.add_eduprogram'
    model = EduProgram
    template_name = "eduprog_list.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['groups'] = {}
        context['form'] = SetProgramToGroupsForm()
        for group in Group.objects.filter(program__isnull=False):
            if group.program.id not in context['groups']:
                context['groups'][group.program.id] = []
            context['groups'][group.program.id].append(group.Name)
        return context

    def get_queryset(self):
        return Teacher.objects.get(user=self.request.user).cathedra.eduprogram_set.all()


@login_required
def get_groups(request):
    result = {}
    if 'program' in request.GET:
        result = list(Group.objects.filter(program__id=request.GET['program']).values('id','Name', 'program'))
        if len(result) < 1:
            result = [{'program': request.GET['program']}]
    return HttpResponse(json.dumps(result), content_type='application/json')


@login_required
@permission_required('umo.change_group', login_url='login')
def set_rup_to_groups(request):
    result = {'result': False}
    form = SetProgramToGroupsForm(request.POST)
    if form.is_valid():
        try:
            program = EduProgram.objects.get(pk=form.cleaned_data['edu_program'])
            groups_in = set(Group.objects.filter(program__id=program.id).values_list('id', flat=True))
            groups_in_form = set(form.cleaned_data['groups'].values_list('id', flat=True))

            for group in Group.objects.filter(id__in=(groups_in - groups_in_form)):
                with transaction.atomic():
                    group.program = None
                    group.save()
                    group.course_set.all().delete()

            for group in form.cleaned_data['groups']:
                with transaction.atomic():
                    gen_subjects = group.program is None
                    if group.program is not None and group.program != program:
                        group.course_set.all().delete()
                        gen_subjects = True
                    group.program = program
                    group.save()
                    if gen_subjects:
                        group.fill_group_disciplines()
            result['result'] = True
            result['program'] = program.id
            result['group_list'] = ', '.join(list(form.cleaned_data['groups'].values_list('Name', flat=True))) if 'groups' in form.cleaned_data else ''
        except Exception as e:
            result['error']='Ошибка при сохранении группы!'
    return HttpResponse(json.dumps(result), content_type='application/json')
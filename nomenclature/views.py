from django.shortcuts import render, redirect
import os

from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from umo.models import Discipline, DisciplineDetails, Semestr, Teacher, Specialization, Profile
from .form import UploadFileForm
from .parseRUP import parseRUP


#from somewhere import handle_uploaded_file

# Create your views here.


@permission_required('umo.add_discipline', login_url='/auth/login')
def rup_list(request):
    return render(request, 'nomenclature.html')


@permission_required('umo.add_discipline', login_url='/auth/login')
def subjects_save(request):
    subjects = request.POST.getlist('disc_id')
    teachers = request.POST.getlist('teachers')
    for i in range(0, len(subjects)):
        subj = Discipline.objects.get(pk=subjects[i])
        subj.lecturer = Teacher.objects.get(pk=teachers[i])
        subj.save()

    return redirect('nomenclatures:select_semestr')


@permission_required('umo.add_discipline', login_url='/auth/login')
def vuborka(request):
    try:
        semestr_id = request.GET['semestr']
        specialization_id = request.GET['specialization']
        profile_id = request.GET['profile']
    except:
        return redirect('nomenclatures:select_semestr')

    semestr = Semestr.objects.get(pk=semestr_id)
    specialization = Specialization.objects.get(pk=specialization_id)
    profile = Profile.objects.get(pk=profile_id)

    disc_filtered = DisciplineDetails.objects.filter(semestr=semestr, subject__program__specialization=specialization, subject__program__profile=profile)
    teachers = Teacher.objects.all()
    disc_filtered  = DisciplineDetails.objects.filter(semestr=semestr, subject__program__specialization=specialization, subject__program__profile=profile)
    teachers = Teacher.objects.all().order_by('FIO')

    return render(request, 'select_teacher.html', {'disciplines': disc_filtered, 'teachers':teachers})


@permission_required('umo.add_discipline', login_url='/auth/login')
def select_semestr(request):
    semestr_list = Semestr.objects.all().order_by('name')
    specialization_list = Specialization.objects.all().order_by('name')
    profile_list = Profile.objects.all().order_by('name')
    return render(request, 'select_semestr.html', {'semestrs':semestr_list, 'specializations':specialization_list, 'profiles':profile_list})


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
            return HttpResponseRedirect(reverse('nomenclatures:success'))

    else:
        form = UploadFileForm()
    return render(request, 'rup_upload.html', {'form': form})


@permission_required('umo.add_discipline', login_url='/auth/login')
def hadle_uploaded_file(filename, file):
     s=os.path.join('upload', filename)
     with open(s, 'wb+') as destination:
         for chunk in file.chunks():
             destination.write(chunk)
     return s





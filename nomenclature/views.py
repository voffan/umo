from django.shortcuts import render, redirect
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from umo.models import Discipline, DisciplineDetails, Semestr, Teacher, Specialization, Profile
from .form import UploadFileForm
from .parseRUP import parseRUP


#from somewhere import handle_uploaded_file


def rup_list(request):
    return render(request, 'nomenclature.html')


def subjects_save(request):
    subjects = request.POST.getlist('disc_id')
    teachers = request.POST.getlist('teachers')
    for i in range(0, len(subjects)):
        subj = Discipline.objects.get(pk=subjects[i])
        subj.lecturer = Teacher.objects.get(pk=teachers[i])
        subj.save()

    return redirect('nomenclatures:select_semestr')


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

    return render(request, 'select_teacher.html', {'disciplines': disc_filtered, 'teachers':teachers})


def select_semestr(request):
    semestrname = Semestr.objects.all()
    specialization_name = Specialization.objects.all()
    profile_name = Profile.objects.all()
    return render(request, 'select_semestr.html', {'semestrs':semestrname, 'specializations':specialization_name, 'profiles':profile_name})


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


def hadle_uploaded_file(filename, file):
     s=os.path.join('upload', filename)
     with open(s, 'wb+') as destination:
         for chunk in file.chunks():
             destination.write(chunk)
     return s





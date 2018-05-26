from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .form import UploadFileForm, SelectTeacher
from umo.models import Discipline, DisciplineDetails, Semestr, Teacher, Specialization, Profile, EduProg
from .parseRUP import parseRUP
from django.core.files.storage import default_storage
from django.conf import settings
import os
#from somewhere import handle_uploaded_file

# Create your views here.


def rup_list(request):
    return render(request, 'nomenclature.html')


def subjects_save(request):
    pass

def vuborka(request):
    semestr_id = request.GET['dropdown1']
    semestr = Semestr.objects.get(pk=semestr_id)

    specialization_id = request.GET['dropdown3']
    specialization = Specialization.objects.get(pk=specialization_id)

    profile_id = request.GET['dropdown4']
    profile = Profile.objects.get(pk=profile_id)

    program =Discipline.objects.filter(program__specialization=specialization, program__profile=profile)

    semestr_choice  = DisciplineDetails.objects.filter(semestr__name=semestr)
    teachers = Teacher.objects.all()
    i = 1

    disp = Discipline.objects.all()
    #discipline = DisciplineDetails.objects.filter(semestr__name=semestr_choice, subject__program__specialization__name=program, subject__Name=disp)


    if request.method == 'POST':
        subjects_save(request)
    return render(request, 'select_teacher.html' , {'disciplines': disp, 'teachers':teachers, 'i':i})



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
            return HttpResponseRedirect(reverse('nomenclatures:select_semestr'))

    else:
        form = UploadFileForm()
    return render(request, 'rup_upload.html', {'form': form})

def hadle_uploaded_file(filename, file):
     s=os.path.join('upload', filename)
     with open(s, 'wb+') as destination:
         for chunk in file.chunks():
             destination.write(chunk)
     return s





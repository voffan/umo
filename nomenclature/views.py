from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .form import UploadFileForm, SelectTeacher
from umo.models import Discipline, DisciplineDetails, Semestr, Teacher, Group
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
    subjects = DisciplineDetails.objects.filter(semestr__name=semestr)
    discipline = Discipline.objects.all()
    teachers = Teacher.objects.all()
    i = 1
    if request.method == 'POST':
        subjects_save(request)
    return render(request, 'select_teacher.html' , {'disciplines': discipline, 'teachers':teachers, 'i':i})



def select_semestr(request):
    semestrname = Semestr.objects.all()
    return render(request, 'select_semestr.html', {'semestrs':semestrname})


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





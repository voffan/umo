from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .form import UploadFileForm
from umo.models import Discipline, DisciplineDetails, Semestr, Teacher
from .parseRUP import parseRUP
from django.core.files.storage import default_storage
from django.conf import settings
import os
#from somewhere import handle_uploaded_file

# Create your views here.

#class RupList(ListView):
#    template_name = 'nomenclature.html'
#    context_object_name = 'nomenclature_list'

def rup_list(request):
    semestrname = Semestr.objects.all()

    return render(request, 'nomenclature.html', {'semestrname': semestrname})

#def vuborka(request):
#    semestr = request.GET['dropdown1']
#   subjects = DisciplineDetails.objects.filter(semestr__name=semestr)
#    teachers = Teacher.objects.filter()

#  if request.method == 'POST':
#        for subject in subjects:

#            for teacher in teachers:
#                print()

def select_semestr(request):
    semestr_name = Semestr.objects.all()
    return render(request, )

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #save_path = os.path.join(settings.MEDIA_ROOT, 'upload', request.FILES['filename'].name)
            #path = default_storage.save(save_path, request.FILES['file'])
            #return default_storage.path(path)
            f=hadle_uploaded_file(request.FILES['file'].name, request.FILES['file'])
            parseRUP(f)
            return HttpResponseRedirect(reverse('nomenclatures:rup_list'))

    else:
        form = UploadFileForm()
    return render(request, 'rup_upload.html', {'form': form})

def hadle_uploaded_file(filename, file):
     s=os.path.join('upload', filename)
     with open(s, 'wb+') as destination:
         for chunk in file.chunks():
             destination.write(chunk)
     return s





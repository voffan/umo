from django.views.generic import ListView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .form import UploadFileForm
from django.core.files.storage import default_storage
from django.conf import settings
import os
#from somewhere import handle_uploaded_file

# Create your views here.

#class RupList(ListView):
#    template_name = 'nomenclature.html'
#    context_object_name = 'nomenclature_list'

def rup_list(request):
    return render(request,'nomenclature.html')

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            #save_path = os.path.join(settings.MEDIA_ROOT, 'upload', request.FILES['filename'].name)
            #path = default_storage.save(save_path, request.FILES['file'])
            #return default_storage.path(path)
            hadle_uploaded_file(request.FILES['file'].name, request.FILES['file'])
            return HttpResponseRedirect(reverse('nomenclatures:rup_list'))

    else:
        form = UploadFileForm()
    return render(request, 'rup_upload.html', {'form': form})

def hadle_uploaded_file(filename, file):
     with open(os.path.join('upload',filename), 'wb+') as destination:
         for chunk in file.chunks():
             destination.write(chunk)

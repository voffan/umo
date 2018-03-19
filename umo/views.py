from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from  django.urls import reverse_lazy
from .models import Person, Teacher

# Create your views here.
class TeacherCreate(CreateView):
    model = Person, Teacher
    fields = '__all__'

class TeacherUpdate(UpdateView):
    model = Person, Teacher
    fields = ['FIO', 'position', 'zvanie']

class TeacherDelete(DeleteView):
    model = Teacher
    success_url = reverse_lazy('teacher')

def list_teachers(request):
    return render(request,'teachers_list.html')
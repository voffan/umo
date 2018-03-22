from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Person, Teacher, Student, GroupList

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

class StudentCreate(CreateView):
    model = Person, Student
    fields = '__all__'
    template_name = 'student_form.html'

class StudentUpdate(UpdateView):
    model = Person, Student
    fields = ['FIO', 'StudentID']

class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('student')

def list_students(request):
    students = GroupList.objects.all()
    context = {}
    context['student_list'] = students
    return render(request,'students_list.html', context)
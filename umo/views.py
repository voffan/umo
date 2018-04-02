from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Person, Teacher, Student, GroupList
from sys import stderr

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
    all = Teacher.objects.all()
    return render(request,'teachers_list.html', {'teachers':all})

def create_teacher(request):
    return render(request, 'teacher_form.html')

class StudentListView(ListView):
    model = GroupList
    context_object_name = 'student_list'
    template_name = "students_list.html"

class StudentCreateView(CreateView):
    model = GroupList
    fields = [ 'group' ]
    success_url = reverse_lazy('student_changelist')
    template_name = "student_form.html"

    def form_valid(self, form):
        student_ = Student.objects.create()
        student_.FIO = form.data.get('fio')
        student_.StudentID = form.data.get('studid')
        student_.save()
        grouplist_ = form.save(commit=False)
        grouplist_.student = student_
        grouplist_.active = True
        grouplist_.save()
        return super().form_valid(form)

class GroupListCreateView(CreateView):
    model = GroupList
    fields = ('group', 'active')
    success_url = reverse_lazy('student_changelist')
    template_name = "student_form.html"

class StudentUpdateView(UpdateView):
    model = GroupList
    fields = ('student.FIO', 'student.StudentID', 'group', 'active')
    success_url = reverse_lazy('student_changelist')
    template_name = "student_form.html"
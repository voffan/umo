from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token
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
    all = Teacher.objects.all()
    return render(request,'teachers_list.html', {'teachers':all})

@requires_csrf_token
def create_teacher(request):
    arg = {}
    #arg['form']
    if request.method == 'POST':
        FIO = request.POST.get('FIO', '')
        Position = request.POST.get('Position', '')
        Zvanie = request.POST.get('Zvanie', '')
    return render(request, 'teacher_form.html')


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
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from .models import Person, Teacher, Student, GroupList
from umo.forms import AddTeacherForm
from django.http import HttpResponseRedirect


# Create your views here.
class TeacherCreateView(CreateView):
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
     if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('teachers:list_teachers'))
        return render(request, 'teacher_form.html', {'form': form})
     form = AddTeacherForm()
     return render(request, 'teacher_form.html', {'form': form})


class StudentListView(ListView):
    model = GroupList
    context_object_name = 'student_list'
    success_url = reverse_lazy('student_changelist')
    template_name = "students_list.html"


class StudentCreateView(CreateView):
    model = GroupList
    fields = { 'group' }
    labels = {
        'group': ('Группа'),
    }
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


def student_delete(request):
    if request.method == 'POST':
        student_ = Student.objects.get(StudentID = request.POST['item_id'])
        grouplist_ = GroupList.objects.get(student__id = student_.id)
        grouplist_.delete()
        student_.delete()
        return HttpResponseRedirect(reverse_lazy('student_changelist'))

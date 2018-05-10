from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Person, Teacher, Student, GroupList, BRSpoints, CheckPoint, Discipline, ExamMarks
from umo.forms import AddTeacherForm
from django.http import HttpResponseRedirect, HttpResponse
from django import template
from django.template import RequestContext


# Create your views here.
class TeacherCreateView(CreateView):
    model = Person, Teacher
    fields = '__all__'


class TeacherUpdate(UpdateView):
    template_name = 'teacher_edit.html'
    success_url = reverse_lazy('teachers:list_teachers')
    model = Teacher
    fields = [
            'FIO',
            'Position',
            'Zvanie',
            'cathedra'
    ]
    labels = {
        'FIO': 'ФИО',
        'Position': 'Должность',
        'Zvanie': 'Звание',
        'cathedra': 'Кафедра'
    }


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
    fields = ['group']
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


# def student_edit(request,student_id):
#     if request.method == "POST":
#         pass
#     gl = GroupList.objects.get(pk=student_id)
#     form = StudentCreateView(instance=gl)
#     return render(request, 'student_form.html', {'form': form})


class StudentUpdateView(UpdateView):
    model = GroupList
    fields = ['group']
    success_url = reverse_lazy('student_changelist')
    template_name = "student_update.html"
    context_object_name = 'student_list'

    def form_valid(self, form):
        student_ = self.object.student
        student_.FIO = form.data.get('fio')
        student_.StudentID = form.data.get('studid')
        student_.save()
        grouplist_ = self.object
        grouplist_.student = student_
        grouplist_.active = True
        grouplist_.save()
        return super().form_valid(form)


def delete_teacher(request):
    if request.method == 'POST':
        teacher_ = Teacher.objects.get(pk=request.POST['teacher'])
        teacher_.delete()
        return HttpResponseRedirect(reverse('teachers:list_teachers'))

class BRSPointsListView(ListView):
    model = BRSpoints
    context_object_name = 'brs_students_list'
    success_url = reverse_lazy('disciplines:disciplines_list')
    template_name = "brs_students.html"

    def get_queryset(self):
        return BRSpoints.objects.filter(brs__discipline__id = self.kwargs['pk']).filter(CheckPoint__id = 1)

    def get_context_data(self, **kwargs):
        context = super(BRSPointsListView, self).get_context_data(**kwargs)
        checkpoint = CheckPoint.objects.all()
        student = Student.objects.all()
        context['checkpoint'] = checkpoint
        discipline = Discipline.objects.get(id=self.kwargs['pk'])
        context['discipline'] = discipline
        dict = {}
        for st in student:
            dict[str(st.id)] = {}
            dict[str(st.id)]['key'] = st.id
            i = 0
            for ch in checkpoint:
                i = i + 1
                dict[str(st.id)][str(i)] = BRSpoints.objects.filter(brs__discipline__id = discipline.id).filter(CheckPoint = ch).get(student = st)
            dict[str(st.id)]['6'] = ExamMarks.objects.filter(exam__discipline__id = discipline.id).get(student = st)
        context['dict'] = dict
        return context

    def post(self, request, *args, **kwargs):
        studid = request.POST.getlist('studid')
        points = []
        points.append(request.POST.getlist('points1'))
        points.append(request.POST.getlist('points2'))
        points.append(request.POST.getlist('points3'))
        points.append(request.POST.getlist('points4'))
        points.append(request.POST.getlist('points5'))
        points.append(request.POST.getlist('points6'))
        arr_size = len(studid)
        checkpoint = CheckPoint.objects.all()
        discipline = Discipline.objects.get(id=self.kwargs['pk'])
        for i in range(0, arr_size):
            st = Student.objects.get(id = studid[i])
            k = 0
            for ch in checkpoint:
                brspoints = BRSpoints.objects.filter(brs__discipline__id = discipline.id).filter(CheckPoint = ch).get(student = st)
                brspoints.points = float(points[k][i].replace(',','.'))
                brspoints.save()
                k = k + 1
            exammarks = ExamMarks.objects.filter(exam__discipline__id = discipline.id).get(student = st)
            exammarks.examPoints = float(points[5][i].replace(',','.'))
            exammarks.inPoints = float(points[3][i].replace(',','.'))
            exammarks.save()
        return HttpResponseRedirect(self.success_url)
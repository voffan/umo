from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from .models import Person, Teacher, Student, GroupList, BRSpoints, CheckPoint, Discipline, ExamMarks, BRS, Mark, MarkSymbol, Exam
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

    def get_context_data(self, **kwargs):
        context = super(StudentCreateView, self).get_context_data(**kwargs)
        context['title'] = "Добавление студента"
        return context

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
        student_ = Student.objects.get(id = request.POST['item_id'])
        grouplist_ = GroupList.objects.get(student__id = student_.id)
        grouplist_.active = False
        return HttpResponseRedirect(reverse_lazy('student_changelist'))


class StudentUpdateView(UpdateView):
    model = GroupList
    fields = ['group']
    success_url = reverse_lazy('student_changelist')
    template_name = "student_form.html"
    context_object_name = 'student_list'

    def get_context_data(self, **kwargs):
        context = super(StudentUpdateView, self).get_context_data(**kwargs)
        context['title'] = "Изменение студента"
        return context

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
    model = GroupList
    context_object_name = 'students_list'
    success_url = reverse_lazy('disciplines:disciplines_list')
    template_name = "brs_students.html"

    def get_queryset(self):
        disc = Discipline.objects.get(id = self.kwargs['pk'])
        return GroupList.objects.filter(group__program = disc.program)

    def get_context_data(self, **kwargs):
        context = super(BRSPointsListView, self).get_context_data(**kwargs)
        checkpoint = CheckPoint.objects.all()
        if (checkpoint.count() < 5):
            if (checkpoint.count() > 0):
                i = 0
                for ch in checkpoint:
                    i = i + 1
                    if (i == 1):
                        ch.Name = "Первый срез"
                    elif (i == 2):
                        ch.Name = "Второй срез"
                    elif (i == 3):
                        ch.Name = "Рубежный срез"
                    else:
                        ch.Name = "Рубежный срез с премиальными баллами"
                    ch.save()
            for i in range(checkpoint.count(), 5):
                ch = CheckPoint()
                if (i == 1):
                    ch.Name = "Первый срез"
                elif (i == 2):
                    ch.Name = "Второй срез"
                elif (i == 3):
                    ch.Name = "Рубежный срез"
                elif (i == 4):
                    ch.Name = "Рубежный срез с премиальными баллами"
                else:
                    ch.Name = "Всего баллов"
                ch.save()
        context['checkpoint'] = checkpoint
        discipline = Discipline.objects.get(id=self.kwargs['pk'])
        context['discipline'] = discipline
        context['grouplist'] = GroupList.objects.all()
        student = Student.objects.all()
        dict = {}
        for st in student:
            dict[str(st.id)] = {}
            dict[str(st.id)]['key'] = st.id
            i = 0
            for ch in checkpoint:
                i = i + 1
                try:
                    dict[str(st.id)][str(i)] = BRSpoints.objects.filter(brs__discipline__id = discipline.id).filter(CheckPoint = ch).get(student = st)
                except BRSpoints.DoesNotExist:
                    dict[str(st.id)][str(i)] = BRSpoints()
                    dict[str(st.id)][str(i)].student = st
                    dict[str(st.id)][str(i)].CheckPoint = ch
                    dict[str(st.id)][str(i)].points = 0.0
                    dict[str(st.id)][str(i)].brs = BRS.objects.filter(discipline__id = discipline.id).first()
                    dict[str(st.id)][str(i)].save()
            try:
                dict[str(st.id)]['6'] = ExamMarks.objects.filter(exam__discipline__id = discipline.id).get(student = st)
            except ExamMarks.DoesNotExist:
                dict[str(st.id)]['6'] = ExamMarks()
                dict[str(st.id)]['6'].student = st
                dict[str(st.id)]['6'].inPoints = 0.0
                dict[str(st.id)]['6'].examPoints = 0.0
                try:
                    dict[str(st.id)]['6'].markSymbol = MarkSymbol.objects.get(name='F')
                except:
                    dict[str(st.id)]['6'].markSymbol = MarkSymbol()
                    dict[str(st.id)]['6'].markSymbol.name = 'F'
                    dict[str(st.id)]['6'].markSymbol.save()
                try:
                    dict[str(st.id)]['6'].mark = Mark.objects.get(name='неуд')
                except:
                    dict[str(st.id)]['6'].mark = Mark()
                    dict[str(st.id)]['6'].mark.name = 'неуд'
                    dict[str(st.id)]['6'].mark.save()
                    dict[str(st.id)]['6'].save()
                dict[str(st.id)]['6'].exam = Exam.objects.filter(discipline__id = discipline.id).first()
                dict[str(st.id)]['6'].save()
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

            totalPoints = exammarks.examPoints + exammarks.inPoints

            if (totalPoints >= 95):
                tempMarkSymbol = 'A'
                tempMark = 'отл'
            elif (totalPoints >= 85):
                tempMarkSymbol = 'B'
                tempMark = 'отл'
            elif (totalPoints >= 75):
                tempMarkSymbol = 'C'
                tempMark = 'хор'
            elif (totalPoints >= 65):
                tempMarkSymbol = 'D'
                tempMark = 'хор'
            elif (totalPoints >= 55):
                tempMarkSymbol = 'E'
                tempMark = 'удовл'
            elif (totalPoints >= 25):
                tempMarkSymbol = 'FX'
                tempMark = 'неуд'
            else:
                tempMarkSymbol = 'F'
                tempMark = 'неуд'

            try:
                exammarks.markSymbol = MarkSymbol.objects.get(name = tempMarkSymbol)
            except:
                exammarks.markSymbol = MarkSymbol()
                exammarks.markSymbol.name = tempMarkSymbol
                exammarks.markSymbol.save()

            try:
                exammarks.mark = Mark.objects.get(name = tempMark)
            except:
                exammarks.mark = Mark()
                exammarks.mark.name = tempMark
                exammarks.mark.save()

            exammarks.save()
        return HttpResponseRedirect(self.success_url)
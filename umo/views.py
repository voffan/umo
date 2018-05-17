from datetime import *
from umo.models import *

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from umo.forms import AddTeacherForm
from django.http import HttpResponseRedirect, HttpResponse
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Alignment, Protection, Font, Side


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

def get_mark(value):
    if (value >= 85):
        return 'отл'
    elif (value >= 65):
        return 'хор'
    elif (value >= 55):
        return 'удовл'
    else:
        return 'неуд'

def get_mark_vedomost(inPoints, examPoints):
    if (inPoints < 45):
        return 'Не допущен'
    value = inPoints + examPoints
    if (value >= 85):
        return 'Отлично'
    elif (value >= 65):
        return 'Хорошо'
    elif (value >= 55):
        return 'Удовлетворительно'
    else:
        return 'Неудовлетворительно'

def get_markSymbol(value):
    if (value >= 95):
        return 'A'
    elif (value >= 85):
        return 'B'
    elif (value >= 75):
        return 'C'
    elif (value >= 65):
        return 'D'
    elif (value >= 55):
        return 'E'
    elif (value >= 25):
        return 'FX'
    else:
        return 'F'


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
        context['control_type'] = 'Баллы ' + discipline.control.controltype.lower()
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
        if (request.POST.get('save')):
            studid = request.POST.getlist('studid')
            points = []
            points.append(request.POST.getlist('points1'))
            points.append(request.POST.getlist('points2'))
            points.append(request.POST.getlist('points3'))
            points.append(request.POST.getlist('points4'))
            points.append(request.POST.getlist('points6'))
            arr_size = len(studid)
            checkpoint = CheckPoint.objects.all()
            discipline = Discipline.objects.get(id=self.kwargs['pk'])
            for i in range(0, arr_size):
                st = Student.objects.get(id=studid[i])
                k = 0

                exammarks = ExamMarks.objects.filter(exam__discipline__id=discipline.id).get(student=st)
                exammarks.examPoints = float(points[4][i].replace(',', '.'))
                exammarks.inPoints = float(points[3][i].replace(',', '.'))

                totalPoints = exammarks.examPoints + exammarks.inPoints

                for ch in checkpoint:
                    brspoints = BRSpoints.objects.filter(brs__discipline__id=discipline.id).filter(CheckPoint=ch).get(
                        student=st)
                    if (k != 4):
                        brspoints.points = float(points[k][i].replace(',', '.'))
                        k = k + 1
                    else:
                        brspoints.points = totalPoints
                        k = 0
                    brspoints.save()

                tempMarkSymbol = get_markSymbol(totalPoints)
                tempMark = get_mark(totalPoints)

                try:
                    exammarks.markSymbol = MarkSymbol.objects.get(name=tempMarkSymbol)
                except:
                    exammarks.markSymbol = MarkSymbol()
                    exammarks.markSymbol.name = tempMarkSymbol
                    exammarks.markSymbol.save()

                try:
                    exammarks.mark = Mark.objects.get(name=tempMark)
                except:
                    exammarks.mark = Mark()
                    exammarks.mark.name = tempMark
                    exammarks.mark.save()

                exammarks.save()
            return HttpResponseRedirect(reverse('brs_studentlist', args=(self.kwargs['pk'])))
        elif (request.POST.get('vedomost')):
            # определяем стили
            font = Font(name='Calibri',
                        size=11,
                        bold=False,
                        italic=False,
                        vertAlign=None,
                        underline='none',
                        strike=False,
                        color='FF000000')

            fill = PatternFill(fill_type='solid',
                               start_color='c1c1c1',
                               end_color='c2c2c2')

            border = Border(left=Side(border_style='thin',
                                      color='FF000000'),
                            right=Side(border_style='thin',
                                       color='FF000000'),
                            top=Side(border_style='thin',
                                     color='FF000000'),
                            bottom=Side(border_style='thin',
                                        color='FF000000'),
                            diagonal=Side(border_style='thin',
                                          color='FF000000'),
                            diagonal_direction=0,
                            outline=Side(border_style='thin',
                                         color='FF000000'),
                            vertical=Side(border_style='thin',
                                          color='FF000000'),
                            horizontal=Side(border_style='thin',
                                            color='FF000000')
                            )
            align_center = Alignment(horizontal='center',
                                     vertical='bottom',
                                     text_rotation=0,
                                     wrap_text=False,
                                     shrink_to_fit=False,
                                     indent=0)
            align_left = Alignment(horizontal='left',
                                   vertical='bottom',
                                   text_rotation=0,
                                   wrap_text=False,
                                   shrink_to_fit=False,
                                   indent=0)
            number_format = 'General'
            protection = Protection(locked=True,
                                    hidden=False)

            # объект
            wb = Workbook()

            # активный лист
            ws = wb.active

            # название страницы
            # ws = wb.create_sheet('первая страница', 0)
            ws.title = 'первая страница'

            # значение ячейки
            # ws['A1'] = "Hello!"

            # текущее время
            today = datetime.today()
            today = today.strftime('%d.%m.%Y %S:%M:%H')

            # данные для строк
            group_name = str(request.POST.get('selected_group'))
            disc_id = self.kwargs['pk']
            exam = Exam.objects.get(discipline__id=disc_id)
            studid = request.POST.getlist('studid')

            inpoints = request.POST.getlist('points4')
            exampoints = request.POST.getlist('points6')
            arr_size = len(studid)

            _row = 10
            _column = 3

            ws.cell(row=1, column=1).value = 'Ведомость текущей и промежуточной аттестации'
            ws.cell(row=2, column=1).value = 'Семестр: ' + str(
                exam.semestr.name) + '      ' + exam.eduperiod.beginyear + '-' + exam.eduperiod.endyear
            ws.cell(row=3, column=1).value = 'Тип контроля: ' + exam.controlType.name
            ws.cell(row=4, column=1).value = 'Группа: ' + group_name
            ws.cell(row=5, column=1).value = 'Дисциплина: ' + exam.discipline.Name
            ws.cell(row=6, column=1).value = 'ФИО преподавателя: ' + exam.discipline.lecturer.FIO
            ws.cell(row=7, column=1).value = 'Дата проведения зачета/экзамена: ' + exam.examDate
            ws.cell(row=9, column=1).value = 'Фамилия, имя, отчество'
            ws.cell(row=9, column=2).value = '№ зачетной книжки'
            ws.cell(row=9, column=3).value = 'Сумма баллов'
            ws.cell(row=9, column=4).value = 'Баллы экзамен'
            ws.cell(row=9, column=5).value = 'Всего баллов'
            ws.cell(row=9, column=6).value = 'Оценка прописью'
            ws.cell(row=9, column=7).value = 'Буквенный эквивалент'
            ws.cell(row=9, column=8).value = 'Подпись преподавателя'
            for i in range(0, arr_size):
                gl = Student.objects.get(id=studid[i])
                ws.cell(row=_row, column=1).value = gl.FIO
                ws.cell(row=_row, column=2).value = gl.StudentID
                ws.cell(row=_row, column=_column).value = str(float(inpoints[i].replace(',', '.'))).replace('.', ',')
                ws.cell(row=_row, column=_column + 1).value = str(float(exampoints[i].replace(',', '.'))).replace('.', ',')
                totalpoints = float(inpoints[i].replace(',', '.')) + float(exampoints[i].replace(',', '.'))
                ws.cell(row=_row, column=_column + 2).value = str(totalpoints).replace('.', ',')
                ws.cell(row=_row, column=_column + 3).value = get_mark_vedomost(float(inpoints[i].replace(',', '.')), float(exampoints[i].replace(',', '.')))
                ws.cell(row=_row, column=_column + 4).value = get_markSymbol(totalpoints)
                _row += 1

            # шрифты
            ws['A9'].font = font
            # обводка
            ws['A9'].border = border
            # выравнивание
            ws['A9'].alignment = align_center

            # вручную устанавливаем высоту первой строки
            # rd = ws.row_dimensions[1]
            # rd.height = 16

            # увеличиваем все строки по высоте
            max_row = ws.max_row
            i = 1
            while i <= max_row:
                rd = ws.row_dimensions[i]
                rd.height = 16
                i += 1

            # сетка + выравнивание
            for cellObj in ws['A9:H30']:
                for cell in cellObj:
                    # print(cell.coordinate, cell.value)
                    ws[cell.coordinate].border = border
                    ws[cell.coordinate].alignment = align_center

            # выравнивание столбца
            for cellObj in ws['A9:H30']:
                for cell in cellObj:
                    ws[cell.coordinate].alignment = align_left

            # перетягивание ячеек
            # https://stackoverflow.com/questions/13197574/openpyxl-adjust-column-width-size
            dims = {}
            for row in ws.rows:
                for cell in row:
                    if cell.value:
                        dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
            for col, value in dims.items():
                # value * коэфициент
                ws.column_dimensions[col].width = value * 1.5

            # сохранение файла в текущую директорию
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=vedomost.xlsx'

            wb.save(response)

            return response
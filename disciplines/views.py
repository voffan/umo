from datetime import *

from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Alignment, Protection, Font, Side

from umo.models import Discipline, DisciplineDetails, ExamMarks, Group, Discipline


# Create your views here.
# def list(request):
#     all = Discipline.objects.all()
#     return render(request, 'disciplines.html', {'disciplines': all})


# def add_discipline(request):
#     if request.method == 'POST':
#         form = AddDisciplineForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/disciplines/list/')
#         return render(request, 'disciplines_form.html', {'form': form})
#     form = AddDisciplineForm()
#     return render(request, 'disciplines_form.html', {'form': form})


class DisciplineList(ListView):
    template_name = 'disciplines.html'
    context_object_name = 'discipline_list'

    def get_queryset(self):
        return Discipline.objects.all()


class DisciplineCreate(CreateView):
    template_name = 'disciplines_form.html'
    success_url = reverse_lazy('disciplines:details_add')
    model = Discipline
    fields = [
        'Name',
        'code',
        'program',
        'lecturer',
        'control',
    ]


class DisciplineUpdate(UpdateView):
    template_name = 'disciplines_update.html'
    success_url = reverse_lazy('disciplines:disciplines_list')
    model = Discipline
    fields = [
        'Name',
        'code',
        'program',
        'lecturer',
        'control',
    ]


class DisciplineDetail(DetailView):
    template_name = 'disciplines_detail.html'
    model = DisciplineDetails
    context_object_name = 'discipline_detail'


def discipline_detail(request, pk):
    if request.method == 'POST':
        pass
    subject_ = Discipline.objects.get(id=pk)
    details_ = DisciplineDetails.objects.get(subject__id=subject_.id)
    form = DisciplineDetail(object=details_)
    return render(request, 'disciplines_detail.html', {'form': form})


class DetailsCreate(CreateView):
    template_name = 'details_form.html'
    model = DisciplineDetails
    success_url = reverse_lazy('disciplines:disciplines_list')
    fields = [
        'subject',
        'Credit',
        'Lecture',
        'Practice',
        'Lab',
        'KSR',
        'SRS',
        'semestr',
    ]


def discipline_delete(request):
    if request.method == 'POST':
        discipline_ = Discipline.objects.get(pk=request.POST['discipline'])
        discipline_.delete()
        return HttpResponseRedirect(reverse('disciplines:disciplines_list'))


def export_to_excel(request):
        # определяем стили
        group_id = 1
        semestr = 2
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
        group = Group.objects.get(pk=group_id)
        students = group.grouplist_set.all()
        subjects = group.program.discipline_set.filter(disciplinedetails__semestr__name=semestr)

        _row = 2
        _column = 2
        ws.cell(row=1, column=1).value = 'ФИО'
        for s in subjects:
            ws.cell(row=1, column=_column).value = s.Name
            _column += 1
        for gl in students:
            print(gl)
            ws.cell(row=_row, column=1).value = gl.student.FIO
            _column = 2
            for s in subjects:
                mark = ExamMarks.objects.filter(student__id=gl.student.id, exam__discipline__id=s.id).first()
                if mark is not None:
                    ws.cell(row=_row, column=_column).value = mark.mark.name
                    print(mark)
                _column += 1
            _row += 1


        # шрифты
        ws['A3'].font = font
        # обводка
        ws['A3'].border = border
        # выравнивание
        ws['A3'].alignment = align_center

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
        for cellObj in ws['A1:M20']:
            for cell in cellObj:
                # print(cell.coordinate, cell.value)
                ws[cell.coordinate].border = border
                ws[cell.coordinate].alignment = align_center

        # выравнивание столбца
        for cellObj in ws['A2:M20']:
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
        response['Content-Disposition'] = 'attachment; filename=items.xlsx'

        wb.save(response)

        return response
import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Alignment, Protection, Font, Side

from umo.models import Exam, Group, Student, EduPeriod, Course, Course, ExamMarks, GroupList, Control


def get_styles():
    font_main = Font(name='Times New Roman',
                     size=12,
                     bold=False,
                     italic=False,
                     vertAlign=None,
                     underline='none',
                     strike=False,
                     color='FF000000')

    font_bold = Font(name='Times New Roman',
                     size=12,
                     bold=True,
                     italic=False,
                     vertAlign=None,
                     underline='none',
                     strike=False,
                     color='FF000000')

    font_bold_s = Font(name='Times New Roman',
                       size=10,
                       bold=True,
                       italic=False,
                       vertAlign=None,
                       underline='none',
                       strike=False,
                       color='FF000000')

    font_calibri = Font(name='Calibri',
                        size=11,
                        bold=False,
                        italic=False,
                        vertAlign=None,
                        underline='none',
                        strike=False,
                        color='FF000000')

    font_arial = Font(name='Arial Cyr',
                      size=12,
                      bold=False,
                      italic=True,
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
                             vertical='center',
                             text_rotation=0,
                             wrap_text=False,
                             shrink_to_fit=False,
                             indent=0)
    align_center2 = Alignment(horizontal='center',
                              vertical='center',
                              text_rotation=0,
                              wrap_text=True,
                              shrink_to_fit=False,
                              indent=0)
    align_left = Alignment(horizontal='left',
                           vertical='center',
                           text_rotation=0,
                           wrap_text=False,
                           shrink_to_fit=False,
                           indent=0)
    align_right = Alignment(horizontal='right',
                            vertical='center',
                            text_rotation=0,
                            wrap_text=False,
                            shrink_to_fit=False,
                            indent=0)
    header_font = Font(name='Times New Roman',
                             size=9,
                             bold=False,
                             italic=False,
                             vertAlign=None,
                             underline='none',
                             strike=False,
                             color='FF000000')
    return (font_main, font_bold, font_bold_s, font_calibri, font_arial, fill, border, align_center, align_center2, align_left, align_right, header_font)


def discipline_scores_to_excel(course_id):
    # определяем стили
    font_main, font_bold, font_bold_s, font_calibri, font_arial, fill, border, align_center, align_center2, align_left, align_right, header_font = get_styles()
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

    # текущее время
    p = datetime.datetime.now()

    # данные для строк
    course = Course.objects.select_related('group','discipline_detail','lecturer').get(pk=course_id)
    semester = course.discipline_detail.semester
    group = course.group
    checkpoints = course.coursemaxpoints_set.all()
    if not course or not semester or not group or not checkpoints:
        return None
    edu_period = get_object_or_404(EduPeriod, active=True)


    _row = 13
    _column = 4
    k = 1
    z = 0

    for gl in group.grouplist_set.select_related('student', 'group').filter(active=True).order_by('student__FIO'):
        ws.cell(row=_row, column=1).value = str(k)
        ws.cell(row=_row, column=2).value = gl.student.FIO
        ws.cell(row=_row, column=3).value = gl.student.student_id
        totalpoints = 0
        _column = 4
        for points in gl.student.brspoints_set.filter(course__id=course_id):
            ws.cell(row=_row, column=_column).value = str(points.points).replace('.', ',')
            totalpoints += points.points
            _column += 1

        _row += 1
        k += 1
        z += 1

    zk = z + 11
    zp = z + 14

    if course.lecturer is None:
        fio = 'отсутствует'
    else:
        fio = course.lecturer.FIO

    ws.cell(row=1, column=1).value = 'ФГАОУ ВО «Северо-Восточный федеральный университет им.М.К.Аммосова'
    ws.cell(row=2, column=1).value = 'Институт математики и информатики'
    ws.cell(row=4, column=1).value = 'Контрольный лист текущей и промежуточной аттестации'
    ws.cell(row=5, column=1).value = str(edu_period.begin_year) + '-' + str(edu_period.end_year) + ' учебный год'
    ws.cell(row=6, column=2).value = 'Семестр'
    ws.cell(row=6, column=3).value = semester.name
    ws.cell(row=7, column=2).value = 'Курс'
    ws.cell(row=7, column=3).value = group.year
    ws.cell(row=7, column=5).value = 'Группа'
    ws.cell(row=7, column=6).value = group.Name
    ws.cell(row=8, column=2).value = 'Дисциплина:'
    ws.cell(row=8, column=3).value = course.discipline_detail.discipline.Name
    ws.cell(row=9, column=2).value = 'Преподаватель:'
    ws.cell(row=9, column=3).value = fio
    ws.cell(row=11, column=1).value = '№'
    ws.cell(row=11, column=2).value = 'Фамилия, имя, отчество'
    ws.cell(row=11, column=3).value = '№ зачетной книжки'
    ws.cell(row=11, column=4).value = 'Сумма баллов за текущую работу'
    ws.cell(row=11, column=6).value = 'Рубежный срез'
    ws.cell(row=11, column=7).value = 'Баллы за экзамен(бонусные баллы)'
    ws.cell(row=11, column=8).value = 'Всего баллов'
    ws.cell(row=11, column=9).value = 'Оценка прописью'
    ws.cell(row=11, column=10).value = 'Буквенный эквивалент'
    ws.cell(row=11, column=11).value = 'Подпись преподавателя'
    ws.cell(row=12, column=4).value = '1 контр. срез (max=' + str(int(checkpoints.get(checkpoint__id=4).max_point)) + ')'
    ws.cell(row=12, column=5).value = '2 контр. срез (max=' + str(int(checkpoints.get(checkpoint__id=5).max_point)) + ')'


    # объединение ячеек
    ws.merge_cells('A1:K1')
    ws.merge_cells('A2:K2')
    ws.merge_cells('A4:K4')
    ws.merge_cells('A5:K5')
    ws.merge_cells('A11:A12')
    ws.merge_cells('B11:B12')
    ws.merge_cells('C11:C12')
    ws.merge_cells('D11:E11')
    ws.merge_cells('F11:F12')
    ws.merge_cells('G11:G12')
    ws.merge_cells('H11:H12')
    ws.merge_cells('I11:I12')
    ws.merge_cells('J11:J12')
    ws.merge_cells('K11:K12')

    # шрифты
    font_9 = Font(name='Times New Roman',
                  size=9,
                  bold=False,
                  italic=False,
                  vertAlign=None,
                  underline='none',
                  strike=False,
                  color='FF000000')
    ws['A11'].font = font_9
    ws['B11'].font = font_9
    ws['C11'].font = font_9
    ws['D11'].font = font_9
    ws['D12'].font = font_9
    ws['E12'].font = font_9
    ws['F11'].font = font_9
    ws['G11'].font = font_9
    ws['H11'].font = font_9
    ws['I11'].font = font_9
    ws['J11'].font = font_9
    ws['K11'].font = font_9

    ws['A4'].font = font_bold
    ws['A5'].font = font_bold

    # увеличиваем все строки по высоте
    max_row = ws.max_row
    i = 1
    while i <= max_row:
        rd = ws.row_dimensions[i]
        rd.height = 16
        i += 1

    # вручную устанавливаем высоту первой строки
    rd = ws.row_dimensions[11]
    rd.height = 28
    rd = ws.row_dimensions[12]
    rd.height = 36

    # сетка
    for cellObj in ws['A11:K' + str(zk+1)]:
        for cell in cellObj:
            # print(cell.coordinate, cell.value)
            ws[cell.coordinate].border = border

    # выравнивание

    ws['B6'].alignment = align_right
    ws['B7'].alignment = align_right
    ws['B8'].alignment = align_right
    ws['B9'].alignment = align_right
    ws['E7'].alignment = align_right
    ws['C6'].alignment = align_center
    ws['C7'].alignment = align_center

    for cellObj in ws['A13:A' + str(zk+1)]:
        for cell in cellObj:
            cell.alignment = align_center
    for cellObj in ws['C13:K' + str(zk+1)]:
        for cell in cellObj:
            cell.alignment = align_center

    for cellObj in ws['A1:K5']:
        for cell in cellObj:
            # print(cell.coordinate, cell.value)
            ws[cell.coordinate].alignment = align_center

    for cellObj in ws['A11:K12']:
        for cell in cellObj:
            # print(cell.coordinate, cell.value)
            ws[cell.coordinate].alignment = align_center2

    # перетягивание ячеек
    dims = {}
    for cellObj in ws['A11:A' + str(zk)]:
        for cell in cellObj:
            if cell.value:
                dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
    for col, value in dims.items():
        # value * коэфициент
        ws.column_dimensions[col].width = value * 3

    dims = {}
    for cellObj in ws['B11:B' + str(zk)]:
        for cell in cellObj:
            if cell.value:
                dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
    for col, value in dims.items():
        # value * коэфициент
        ws.column_dimensions[col].width = value * 1.2

    return wb


def exam_scores(exam_id):
    font_main, font_bold, font_bold_s, font_calibri, font_arial, fill, border, align_center, align_center2, align_left, align_right, header_font = get_styles()
    number_format = 'General'

    # данные для строк
    exam = Exam.objects.select_related('course').get(id=exam_id)
    group = exam.course.group
    #group_list = GroupList.objects.filter(student__id__in=exam.exammarks_set.all().order_by('student__FIO').values_list('student__id', flat=True))
    exam_points = exam.exammarks_set.all().order_by('student__FIO')
    semester = exam.course.discipline_detail.semester.name
    additional = int(semester)//2 if int(semester) % 2 == 1 else (int(semester) - 1)//2
    edu_period = EduPeriod.objects.get(begin_year__year=group.begin_year.year + additional)

    wb = Workbook()
    # активный лист
    ws = wb.active
    ws.title = 'Экзамен'
    _row = 12
    _column = 4
    k = 1
    z = 0

    marks_total = [0] * 10

    i = 0
    for mark in exam_points:
        ws.cell(row=_row, column=1).value = str(k)
        ws.cell(row=_row, column=2).value = mark.student.FIO
        ws.cell(row=_row, column=3).value = mark.student.student_id
        ws.cell(row=_row, column=_column).value = str(mark.inPoints + mark.additional_points).replace('.', ',')
        ws.cell(row=_row, column=_column + 1).value = str(mark.examPoints).replace('.', ',')
        ws.cell(row=_row, column=_column + 2).value = str(mark.total_points).replace('.', ',')
        ws.cell(row=_row, column=_column + 3).value = ExamMarks.MARKS[mark.mark][1]
        ws.cell(row=_row, column=_column + 4).value = mark.mark_symbol
        marks_total[mark.mark] += 1
        _row += 1
        z += 1
        k += 1

    zk = z + 11
    zp = z + 14
    zp2 = zp + 7

    ws.cell(row=1, column=1).value = 'ФГАОУ ВО «Северо-Восточный федеральный университет им.М.К.Аммосова'
    ws.cell(row=2, column=1).value = 'Институт математики и информатики'
    ws.cell(row=3, column=1).value = 'Ведомость текущей и промежуточной аттестации'
    ws.cell(row=5, column=1).value = 'Семестр: ' + semester + ', ' + str(edu_period.begin_year.year) + '-' + str(edu_period.end_year.year) + ' уч.г.'
    ws.cell(row=6, column=1).value = 'Форма контроля:'
    ws.cell(row=6, column=3).value = Control.CONTROL_FORM[exam.controlType][1]
    ws.cell(row=6, column=5).value = 'курс ' + str(group.year)
    ws.cell(row=6, column=6).value = 'группа:'
    ws.cell(row=6, column=7).value = group.Name
    ws.cell(row=7, column=1).value = 'Дисциплина:'
    ws.cell(row=7, column=3).value = exam.course.discipline_detail.discipline.Name
    ws.cell(row=8, column=1).value = 'Фамилия, имя, отчество преподавателя:'
    ws.cell(row=8, column=4).value = exam.course.lecturer.FIO
    ws.cell(row=9, column=1).value = 'Дата проведения зачета/экзамена:'
    ws.cell(row=9, column=3).value = exam.examDate
    ws.cell(row=11, column=1).value = '№'
    ws.cell(row=11, column=2).value = 'Фамилия, имя, отчество'
    ws.cell(row=11, column=3).value = '№ зачетной книжки'
    ws.cell(row=11, column=4).value = 'Сумма баллов за текущую работу-рубеж.срез'
    ws.cell(row=11, column=5).value = 'Баллы ' + Control.CONTROL_FORM[exam.controlType][1] + ' (бонусные баллы)'
    ws.cell(row=11, column=6).value = 'Всего баллов'
    ws.cell(row=11, column=7).value = 'Оценка прописью'
    ws.cell(row=11, column=8).value = 'Буквенный эквивалент'
    ws.cell(row=11, column=9).value = 'Подпись преподавателя'
    ws.cell(row=zp, column=2).value = 'зачтено'
    ws.cell(row=zp + 1, column=2).value = 'не зачтено'
    ws.cell(row=zp + 2, column=2).value = 'не аттест'
    ws.cell(row=zp + 3, column=2).value = '5(отлично)'
    ws.cell(row=zp + 4, column=2).value = '4(хорошо)'
    ws.cell(row=zp + 5, column=2).value = '3(удовл)'
    ws.cell(row=zp + 6, column=2).value = '2(неудовл)'
    ws.cell(row=zp2, column=2).value = 'неявка'
    ws.cell(row=zp, column=5).value = 'Сумма баллов'
    ws.cell(row=zp + 1, column=5).value = '95-100'
    ws.cell(row=zp + 2, column=5).value = '85-94,9'
    ws.cell(row=zp + 3, column=5).value = '75-84,9'
    ws.cell(row=zp + 4, column=5).value = '65-74,9'
    ws.cell(row=zp + 5, column=5).value = '55-64,9'
    ws.cell(row=zp + 6, column=5).value = '25-54,9'
    ws.cell(row=zp2, column=5).value = '0-24,9'
    ws.cell(row=zp, column=7).value = 'Буквенный эквивалент оценки'
    ws.cell(row=zp + 1, column=7).value = 'A'
    ws.cell(row=zp + 2, column=7).value = 'B'
    ws.cell(row=zp + 3, column=7).value = 'C'
    ws.cell(row=zp + 4, column=7).value = 'D'
    ws.cell(row=zp + 5, column=7).value = 'E'
    ws.cell(row=zp + 6, column=7).value = 'FX'
    ws.cell(row=zp2, column=7).value = 'F'
    ws.cell(row=zp + 10, column=2).value = 'Директор ИМИ СВФУ____________________'
    ws.cell(row=zp + 10, column=4).value = 'В.И.Афанасьева'

    #формат даты
    ws['C9'].number_format = 'DD.MM.YYY'

    # объединение ячеек
    ws.merge_cells('A1:I1')
    ws.merge_cells('A2:I2')
    ws.merge_cells('A3:I3')
    ws.merge_cells('A5:B5')
    ws.merge_cells('A6:B6')
    ws.merge_cells('C6:D6')
    ws.merge_cells('A7:B7')
    ws.merge_cells('C7:G7')
    ws.merge_cells('A8:C8')
    ws.merge_cells('D8:G8')
    ws.merge_cells('A9:B9')
    ws.merge_cells('C9:D9')
    ws.merge_cells('E' + str(zp) + ':F' + str(zp))
    ws.merge_cells('E' + str(zp + 1) + ':F' + str(zp + 1))
    ws.merge_cells('E' + str(zp + 2) + ':F' + str(zp + 2))
    ws.merge_cells('E' + str(zp + 3) + ':F' + str(zp + 3))
    ws.merge_cells('E' + str(zp + 4) + ':F' + str(zp + 4))
    ws.merge_cells('E' + str(zp + 5) + ':F' + str(zp + 5))
    ws.merge_cells('E' + str(zp + 6) + ':F' + str(zp + 6))
    ws.merge_cells('E' + str(zp + 7) + ':F' + str(zp + 7))
    ws.merge_cells('G' + str(zp) + ':H' + str(zp))
    ws.merge_cells('G' + str(zp + 1) + ':H' + str(zp + 1))
    ws.merge_cells('G' + str(zp + 2) + ':H' + str(zp + 2))
    ws.merge_cells('G' + str(zp + 3) + ':H' + str(zp + 3))
    ws.merge_cells('G' + str(zp + 4) + ':H' + str(zp + 4))
    ws.merge_cells('G' + str(zp + 5) + ':H' + str(zp + 5))
    ws.merge_cells('G' + str(zp + 6) + ':H' + str(zp + 6))
    ws.merge_cells('G' + str(zp + 7) + ':H' + str(zp + 7))
    ws.merge_cells('B' + str(zp + 10) + ':C' + str(zp + 10))
    ws.merge_cells('D' + str(zp + 10) + ':E' + str(zp + 10))

    ws.cell(row=zp, column=3).value = str(marks_total[6])
    ws.cell(row=zp + 1, column=3).value = str(marks_total[7])
    ws.cell(row=zp + 2, column=3).value = str(marks_total[8])
    ws.cell(row=zp + 3, column=3).value = str(marks_total[5])
    ws.cell(row=zp + 4, column=3).value = str(marks_total[4])
    ws.cell(row=zp + 5, column=3).value = str(marks_total[3])
    ws.cell(row=zp + 6, column=3).value = str(marks_total[2])
    ws.cell(row=zp2, column=3).value = str(marks_total[0])

    # шрифты
    for cellObj in ws['A1:I' + str(zk)]:
        for cell in cellObj:
            ws[cell.coordinate].font = font_main

    for cellObj in ws['G12:G' + str(zk)]:
        for cell in cellObj:
            ws[cell.coordinate].font = font_bold_s

    for cellObj in ws['B12:B' + str(zk)]:
        for cell in cellObj:
            ws[cell.coordinate].font = font_calibri

    for cellObj in ws['H12:H' + str(zk)]:
        for cell in cellObj:
            ws[cell.coordinate].font = font_calibri

    for cellObj in ws['E12:E' + str(zk)]:
        for cell in cellObj:
            ws[cell.coordinate].font = font_bold

    for cellObj in ws['E11:I11']:
        for cell in cellObj:
            ws[cell.coordinate].font = font_main

    ws['A3'].font = font_bold
    ws['C7'].font = font_bold
    ws['D8'].font = font_bold
    ws['F6'].font = font_bold
    ws['C7'].font = font_arial
    ws['D8'].font = font_arial
    ws['G6'].font = font_arial
    ws['C9'].font = font_arial
    ws['A11'].font = header_font
    ws['B11'].font = header_font
    ws['C11'].font = header_font
    ws['D11'].font = header_font
    ws['E11'].font = header_font
    ws['F11'].font = header_font
    ws['G11'].font = header_font
    ws['H11'].font = header_font
    ws['I11'].font = header_font
    ws['C6'].font = font_arial

    # увеличиваем все строки по высоте
    max_row = ws.max_row
    i = 1
    while i <= max_row:
        rd = ws.row_dimensions[i]
        rd.height = 16
        i += 1

    # вручную устанавливаем высоту первой строки
    rd = ws.row_dimensions[11]
    rd.height = 48

    # сетка
    for cellObj in ws['A11:I' + str(zk)]:
        for cell in cellObj:
            # print(cell.coordinate, cell.value)
            ws[cell.coordinate].border = border

    for cellObj in ws['B' + str(zp) + ':C' + str(zp2)]:
        for cell in cellObj:
            # print(cell.coordinate, cell.value)
            ws[cell.coordinate].border = border

    for cellObj in ws['E' + str(zp) + ':H' + str(zp2)]:
        for cell in cellObj:
            # print(cell.coordinate, cell.value)
            ws[cell.coordinate].border = border

    # выравнивание
    for cellObj in ws['A1:I3' + str(zk)]:
        for cell in cellObj:
            # print(cell.coordinate, cell.value)
            ws[cell.coordinate].alignment = align_center

    for cellObj in ws['A11:I11']:
        for cell in cellObj:
            # print(cell.coordinate, cell.value)
            ws[cell.coordinate].alignment = align_center2

    for cellObj in ws['A5:I9']:
        for cell in cellObj:
            # print(cell.coordinate, cell.value)
            ws[cell.coordinate].alignment = align_left

    for cellObj in ws['B12:B' + str(zk)]:
        for cell in cellObj:
            ws[cell.coordinate].alignment = align_left

    # перетягивание ячеек
    dims = {}
    for cellObj in ws['G11:G' + str(zk)]:
        for cell in cellObj:
            if cell.value:
                dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
    for col, value in dims.items():
        # value * коэфициент
        ws.column_dimensions[col].width = value * 1.5

    dims = {}
    for cellObj in ws['A11:A' + str(zk)]:
        for cell in cellObj:
            if cell.value:
                dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
    for col, value in dims.items():
        # value * коэфициент
        ws.column_dimensions[col].width = value * 3

    dims = {}
    for cellObj in ws['B11:B' + str(zk)]:
        for cell in cellObj:
            if cell.value:
                dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
    for col, value in dims.items():
        # value * коэфициент
        ws.column_dimensions[col].width = value * 1.5

    dims = {}
    for cellObj in ws['D11:D' + str(zk)]:
        for cell in cellObj:
            if cell.value:
                dims[cell.column] = max((dims.get(cell.column, 0), len(cell.value)))
    for col, value in dims.items():
        # value * коэфициент
        ws.column_dimensions[col].width = value * 0.25

    ws.print_area = 'A1:I' + str(zk + 14)
    ws.page_setup.orientation = ws.ORIENTATION_PORTRAIT
    ws.page_setup.paperSize = 9
    ws.page_setup.fitToHeight = False
    ws.page_setup.fitToWidth = True
    ws.page_setup.fitToPage = True
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    #ws.set_printer_settings(paper_size=9, orientation='landscape')
    # сохранение файла в выбранную директорию
    return wb
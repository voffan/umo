import openpyxl
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db import transaction
from openpyxl import load_workbook, Workbook
from openpyxl.styles import PatternFill, Border, Alignment, Protection, Font, Side
from openpyxl.utils.cell import get_column_interval
from hours.models import GroupInfo, Group, EduPeriod, Teacher, Kafedra, DisciplineSetting, CourseHours, HoursSettings, \
    SupervisionHours, PracticeHours, OtherHours, TeacherGekStatus, CathedraEmployee
from umo.models import Discipline, EduProgram, Group, Year, GroupList, Student, EduOrg, Specialization, Profile, \
    Control, DisciplineDetails


def kup_header(ws, teacher):
    year = EduPeriod.objects.filter(active=True).first()
    cathedra = teacher.cathedra.name
    position = teacher.position.name
    teacher_name = str(teacher.FIO).split()
    employee = CathedraEmployee.objects.filter(teacher_id=teacher.id).first()
    ws.cell(row=1, column=1).value = teacher_name[0][0] + teacher_name[1][0] + teacher_name[2][0]
    ws.cell(row=2, column=1).value = 'КАРТОЧКА УЧЕБНЫХ ПОРУЧЕНИЙ на ' + str(year) + ' учебный год'
    ws.cell(row=3, column=1).value = '(плановый набор, первая половина рабочего дня)'
    ws.cell(row=4, column=1).value = 'Кафедра: ' + str(cathedra)
    ws.cell(row=5, column=1).value = 'Преподаватель: ' + str(teacher.FIO)
    ws.cell(row=5, column=13).value = 'Должность: ' + str(position) + ', ставка: ' + str(employee.stavka) + ' став., ' + ' уч. степень: '
    ws.cell(row=6, column=1).value = '№'
    ws.cell(row=6, column=2).value = 'Индекс дисциплины'
    ws.cell(row=6, column=3).value = 'Наименование дисциплин'
    ws.cell(row=6, column=4).value = 'курс'
    ws.cell(row=6, column=5).value = 'название группы'
    ws.cell(row=6, column=6).value = 'Студентов'
    ws.cell(row=6, column=7).value = 'Кол-во групп'
    ws.cell(row=6, column=8).value = 'Кол-во подгрупп'
    ws.cell(row=6, column=9).value = 'Лекции'
    ws.cell(row=6, column=10).value = 'Практ., семин. занятия'
    ws.cell(row=7, column=10).value = 'по плану'
    ws.cell(row=7, column=11).value = 'всего'
    ws.cell(row=6, column=12).value = 'Лабор. занятия'
    ws.cell(row=7, column=12).value = 'по плану'
    ws.cell(row=7, column=13).value = 'всего'
    ws.cell(row=6, column=14).value = 'консультации'
    ws.cell(row=7, column=14).value = 'предэкзаменационные'
    ws.cell(row=6, column=15).value = 'прием'
    ws.cell(row=7, column=15).value = 'Зачетов'
    ws.cell(row=7, column=16).value = 'Экзаменов'
    ws.cell(row=6, column=17).value = 'Проверка, РГР, реф., контрольных работ'
    ws.cell(row=6, column=18).value = 'руководство'
    ws.cell(row=7, column=18).value = 'дипл. проектир'
    ws.cell(row=7, column=19).value = 'курс. работами'
    ws.cell(row=7, column=20).value = 'аспирантами'
    ws.cell(row=7, column=21).value = 'магистрантами'
    ws.cell(row=7, column=22).value = 'программой магистратуры'
    ws.cell(row=6, column=23).value = 'руководство практиками'
    ws.cell(row=7, column=23).value = 'учебная'
    ws.cell(row=7, column=24).value = 'производственная'
    ws.cell(row=7, column=25).value = 'преддипломная'
    ws.cell(row=7, column=26).value = 'педагогическая'
    ws.cell(row=6, column=27).value = 'ГЭК, ГАК'
    ws.cell(row=6, column=28).value = 'Проверка остаточных знаний'
    ws.cell(row=6, column=29).value = 'Рецензирование дипл. работ'
    ws.cell(row=6, column=30).value = 'Прием экзаменов по канд. минимуму'
    ws.cell(row=6, column=31).value = 'Рецензир. рефератов для канд. мин.'
    ws.cell(row=6, column=32).value = 'Контроль СРС'
    ws.cell(row=6, column=33).value = 'Контроль БРС'
    ws.cell(row=6, column=34).value = 'Всего часов к расчету штатов'
    ws.cell(row=6, column=35).value = 'Почасовой фонд (для сторонних)'
    ws.cell(row=6, column=36).value = 'ИТОГО по кафедре'
    ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=36)
    ws.merge_cells(start_row=3, start_column=1, end_row=3, end_column=36)
    ws.merge_cells(start_row=6, start_column=1, end_row=7, end_column=1)
    ws.merge_cells(start_row=6, start_column=2, end_row=7, end_column=2)
    ws.merge_cells(start_row=6, start_column=3, end_row=7, end_column=3)
    ws.merge_cells(start_row=6, start_column=4, end_row=7, end_column=4)
    ws.merge_cells(start_row=6, start_column=5, end_row=7, end_column=5)
    ws.merge_cells(start_row=6, start_column=6, end_row=7, end_column=6)
    ws.merge_cells(start_row=6, start_column=7, end_row=7, end_column=7)
    ws.merge_cells(start_row=6, start_column=8, end_row=7, end_column=8)
    ws.merge_cells(start_row=6, start_column=9, end_row=7, end_column=9)
    ws.merge_cells(start_row=6, start_column=10, end_row=6, end_column=11)
    ws.merge_cells(start_row=6, start_column=12, end_row=6, end_column=13)
    ws.merge_cells(start_row=6, start_column=15, end_row=6, end_column=16)
    ws.merge_cells(start_row=6, start_column=17, end_row=7, end_column=17)
    ws.merge_cells(start_row=6, start_column=18, end_row=6, end_column=22)
    ws.merge_cells(start_row=6, start_column=23, end_row=6, end_column=26)
    ws.merge_cells(start_row=6, start_column=27, end_row=7, end_column=27)
    ws.merge_cells(start_row=6, start_column=28, end_row=7, end_column=28)
    ws.merge_cells(start_row=6, start_column=29, end_row=7, end_column=29)
    ws.merge_cells(start_row=6, start_column=30, end_row=7, end_column=30)
    ws.merge_cells(start_row=6, start_column=31, end_row=7, end_column=31)
    ws.merge_cells(start_row=6, start_column=32, end_row=7, end_column=32)
    ws.merge_cells(start_row=6, start_column=33, end_row=7, end_column=33)
    ws.merge_cells(start_row=6, start_column=34, end_row=7, end_column=34)
    ws.merge_cells(start_row=6, start_column=35, end_row=7, end_column=35)
    ws.merge_cells(start_row=6, start_column=36, end_row=7, end_column=36)
    ws.row_dimensions[6].height = float(33.75)
    ws.row_dimensions[7].height = float(150.00)
    ws.column_dimensions['C'].width = float(50.00)
    ws.column_dimensions['E'].width = float(20.00)
    ws.cell(row=2, column=1).alignment = Alignment(horizontal='center', vertical='center')
    ws.cell(row=3, column=1).alignment = Alignment(horizontal='center', vertical='center')
    ws.cell(row=6, column=1).alignment = Alignment(horizontal='center', vertical='center')
    ws.cell(row=6, column=2).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=3).alignment = Alignment(horizontal='center', vertical='center')
    ws.cell(row=6, column=4).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=5).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=6).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=7).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=8).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=9).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=10).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
    ws.cell(row=6, column=12).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
    ws.cell(row=6, column=14).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
    ws.cell(row=6, column=18).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
    ws.cell(row=6, column=23).alignment = Alignment(wrap_text=True, horizontal='center', vertical='center')
    ws.cell(row=7, column=10).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=11).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=12).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=13).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=14).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=15).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=16).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=17).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=18).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=19).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=20).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=21).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=22).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=23).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=24).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=25).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=7, column=26).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=27).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=28).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=29).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=30).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=31).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=32).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=33).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=34).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=35).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)
    ws.cell(row=6, column=36).alignment = Alignment(horizontal='center', vertical='center', textRotation=90)


def kup_body(ws, teacher):
    start = 9
    year = EduPeriod.objects.filter(active=True).first()
    courses = CourseHours.objects.filter(teacher_id=teacher.id, edu_period=year)
    ws.cell(row=start, column=2).value = 'Первый семестр'
    for course in courses:
        supervision = SupervisionHours.objects.filter(teacher_id=teacher.id, edu_period=year,
                                                      group=course.group)
        practice = PracticeHours.objects.filter(teacher_id=teacher.id, edu_period=year, group=course.group)
        other = OtherHours.objects.filter(teacher_id=teacher.id, edu_period=year, group=course.group)
        if int(course.discipline_settings.semester.name) % 2 != 0:
            if course.group.edu_type == 1:
                start = start + 1
                ws.cell(row=start, column=2).value = 'Очная форма обучения'
                kup_body_data(ws, start, course, supervision, practice, other)
                start = start + 1
            if course.group.edu_type == 2:
                start = start + 1
                ws.cell(row=start, column=2).value = 'Заочная форма обучения'
                kup_body_data(ws, start, course, supervision, practice, other)
                start = start + 1
            if course.group.edu_type == 3:
                start = start + 1
                ws.cell(row=start, column=2).value = 'Очно-заочная форма обучения'
                kup_body_data(ws, start, course, supervision, practice, other)
                start = start + 1
    start = start + 1
    ws.cell(row=start, column=3).value = 'Итого за 1 семестр'
    ws.cell(row=start, column=9).value = '=SUM(I11:I' + str(start-1) + ')'
    ws.cell(row=start, column=10).value = '=SUM(J11:J' + str(start-1) + ')'
    ws.cell(row=start, column=11).value = 0
    ws.cell(row=start, column=12).value = 0
    ws.cell(row=start, column=13).value = 0
    ws.cell(row=start, column=14).value = 0
    ws.cell(row=start, column=15).value = 0
    ws.cell(row=start, column=16).value = 0
    ws.cell(row=start, column=17).value = 0
    ws.cell(row=start, column=18).value = 0
    ws.cell(row=start, column=19).value = 0
    ws.cell(row=start, column=20).value = 0
    ws.cell(row=start, column=21).value = 0
    ws.cell(row=start, column=22).value = 0
    ws.cell(row=start, column=23).value = 0
    ws.cell(row=start, column=24).value = 0
    ws.cell(row=start, column=25).value = 0
    ws.cell(row=start, column=27).value = 0
    ws.cell(row=start, column=28).value = 0
    ws.cell(row=start, column=29).value = 0
    ws.cell(row=start, column=30).value = 0
    ws.cell(row=start, column=31).value = 0
    ws.cell(row=start, column=32).value = 0
    ws.cell(row=start, column=33).value = 0
    ws.cell(row=start, column=34).value = 0
    ws.cell(row=start, column=35).value = 0
    ws.cell(row=start, column=36).value = 0
    start = start + 2
    ws.cell(row=start, column=2).value = 'Второй семестр'
    ws.merge_cells(start_row=start, start_column=2, end_row=start, end_column=36)
    for course in courses:
        if int(course.discipline_settings.semester.name) % 2 == 0:
            if course.group.edu_type == 1:
                start = start + 1
                ws.cell(row=start, column=2).value = 'Очная форма обучения'
                kup_body_data(ws, start, course, supervision, practice, other)
                start = start + 1
            if course.group.edu_type == 2:
                start = start + 1
                ws.cell(row=start, column=2).value = 'Заочная форма обучения'
                kup_body_data(ws, start, course, supervision, practice, other)
                start = start + 1
            if course.group.edu_type == 3:
                start = start + 1
                ws.cell(row=start+1, column=2).value = 'Очно-заочная форма обучения'
                kup_body_data(ws, start, course, supervision, practice, other)
                start = start + 1
    start = start + 1
    ws.cell(row=start, column=3).value = 'Итого за 2 семестр'
    ws.cell(row=start, column=9).value = '=SUM(I11:I' + str(start - 1) + ')'
    ws.cell(row=start, column=10).value = '=SUM(J11:J' + str(start - 1) + ')'
    ws.cell(row=start, column=11).value = 0
    ws.cell(row=start, column=12).value = 0
    ws.cell(row=start, column=13).value = 0
    ws.cell(row=start, column=14).value = 0
    ws.cell(row=start, column=15).value = 0
    ws.cell(row=start, column=16).value = 0
    ws.cell(row=start, column=17).value = 0
    ws.cell(row=start, column=18).value = 0
    ws.cell(row=start, column=19).value = 0
    ws.cell(row=start, column=20).value = 0
    ws.cell(row=start, column=21).value = 0
    ws.cell(row=start, column=22).value = 0
    ws.cell(row=start, column=23).value = 0
    ws.cell(row=start, column=24).value = 0
    ws.cell(row=start, column=25).value = 0
    ws.cell(row=start, column=27).value = 0
    ws.cell(row=start, column=28).value = 0
    ws.cell(row=start, column=29).value = 0
    ws.cell(row=start, column=30).value = 0
    ws.cell(row=start, column=31).value = 0
    ws.cell(row=start, column=32).value = 0
    ws.cell(row=start, column=33).value = 0
    ws.cell(row=start, column=34).value = 0
    ws.cell(row=start, column=35).value = 0
    ws.cell(row=start, column=36).value = 0
    start = start + 1
    ws.cell(row=start, column=3).value = 'Всего часов плановых'
    ws.cell(row=start, column=9).value = '=SUM(I11:I' + str(start - 1) + ')'
    ws.cell(row=start, column=10).value = '=SUM(J11:J' + str(start - 1) + ')'
    ws.cell(row=start, column=11).value = 0
    ws.cell(row=start, column=12).value = 0
    ws.cell(row=start, column=13).value = 0
    ws.cell(row=start, column=14).value = 0
    ws.cell(row=start, column=15).value = 0
    ws.cell(row=start, column=16).value = 0
    ws.cell(row=start, column=17).value = 0
    ws.cell(row=start, column=18).value = 0
    ws.cell(row=start, column=19).value = 0
    ws.cell(row=start, column=20).value = 0
    ws.cell(row=start, column=21).value = 0
    ws.cell(row=start, column=22).value = 0
    ws.cell(row=start, column=23).value = 0
    ws.cell(row=start, column=24).value = 0
    ws.cell(row=start, column=25).value = 0
    ws.cell(row=start, column=27).value = 0
    ws.cell(row=start, column=28).value = 0
    ws.cell(row=start, column=29).value = 0
    ws.cell(row=start, column=30).value = 0
    ws.cell(row=start, column=31).value = 0
    ws.cell(row=start, column=32).value = 0
    ws.cell(row=start, column=33).value = 0
    ws.cell(row=start, column=34).value = 0
    ws.cell(row=start, column=35).value = 0
    ws.cell(row=start, column=36).value = 0
    start = start +2
    teacher_name = str(teacher.FIO).split()
    ws.cell(row=start, column=3).value = 'Преподаватель'
    ws.cell(row=start, column=6).value = '/' + teacher_name[1][0] + '.' + teacher_name[2][0] + '. ' + teacher_name[0]
    ws.cell(row=start, column=15).value = 'Зав. кафедрой'
    ws.cell(row=start, column=21).value = '/Н.В. Николаева'
    ws.cell(row=start, column=27).value = 'Дата:'
    ws.cell(row=start, column=3).alignment = Alignment(horizontal='right')
    ws.cell(row=start, column=4).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=5).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=6).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=7).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=8).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=18).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=19).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=20).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=21).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=22).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=23).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=28).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=29).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=30).border = Border(bottom=Side(style='thin'))
    ws.cell(row=start, column=31).border = Border(bottom=Side(style='thin'))
    #ws.cell(start_row=1, start_column=1, end_row=start-2, end_column=36).border = Border(top=Side(style='thin'), bottom=Side(style='thin'), left=Side(style='thin'), right=Side(style='thin'))


def kup_body_data(ws, start, course, supervision, practice, other):
    start = start + 1
    ws.cell(row=start, column=2).value = course.discipline_settings.discipline.code
    ws.cell(row=start, column=3).value = course.discipline_settings.discipline.Name
    semester = int(course.discipline_settings.semester.name)
    # if semester == 1 or 2:
    #     ws.cell(row=start, column=4).value = 1
    # elif semester == 3 or 4:
    #     ws.cell(row=start, column=4).value = 2
    # elif semester == 5 or 6:
    #     ws.cell(row=start, column=4).value = 3
    # elif semester == 7 or 8:
    #     ws.cell(row=start, column=4).value = 4
    ws.cell(row=start, column=5).value = course.group.group.Name
    ws.cell(row=start, column=6).value = course.group.amount
    ws.cell(row=start, column=7).value = 1
    ws.cell(row=start, column=8).value = course.group.subgroup
    ws.cell(row=start, column=11).value = course.f_lecture
    ws.cell(row=start, column=10).value = course.discipline_settings.Practice
    ws.cell(row=start, column=11).value = course.f_practice
    ws.cell(row=start, column=12).value = course.discipline_settings.Lab
    ws.cell(row=start, column=13).value = course.f_lab
    ws.cell(row=start, column=14).value = course.f_consult_hours
    ws.cell(row=start, column=17).value = course.f_control_hours
    if supervision:
        supervision0 = supervision.filter(supervision_type=1).first()
        supervision1 = supervision.filter(supervision_type=2).first()
        supervision2 = supervision.filter(supervision_type=3).first()
        supervision3 = supervision.filter(supervision_type=4).first()
        supervision4 = supervision.filter(supervision_type=5).first()
        ws.cell(row=start, column=18).value = int(supervision0.hours)
        ws.cell(row=start, column=19).value = int(supervision1.hours)
        ws.cell(row=start, column=20).value = int(supervision2.hours)
        ws.cell(row=start, column=21).value = int(supervision3.hours)
        ws.cell(row=start, column=22).value = int(supervision4.hours)
    if practice:
        practice0 = practice.filter(practice_type=1).first()
        practice1 = practice.filter(practice_type=2).first()
        practice2 = practice.filter(practice_type=3).first()
        practice3 = practice.filter(practice_type=4).first()
        ws.cell(row=start, column=23).value = int(practice0.hours)
        ws.cell(row=start, column=24).value = int(practice1.hours)
        ws.cell(row=start, column=25).value = int(practice2.hours)
        ws.cell(row=start, column=26).value = int(practice3.hours)
    if other:
        other0 = other.filter(other_type=1).first()
        other1 = other.filter(other_type=2).first()
        other2 = other.filter(other_type=3).first()
        other3 = other.filter(other_type=4).first()
        ws.cell(row=start, column=27).value = int(other0.hours)
        ws.cell(row=start, column=29).value = int(other1.hours)
        ws.cell(row=start, column=30).value = int(other2.hours)
        ws.cell(row=start, column=31).value = int(other3.hours)
    ws.cell(row=start, column=32).value = course.f_control_SRS
    ws.cell(row=start, column=33).value = course.f_control_BRS
    start += 1


def kup_export(teacher):
    wb = Workbook()
    ws = wb.active
    ws.title = teacher.FIO
    kup_header(ws, teacher)
    kup_body(ws, teacher)
    wb.save('KUP.xlsx')
    return wb


def schedule_request():
    pass


def attachment():
    pass

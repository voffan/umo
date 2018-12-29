from datetime import *

from django.db import models, transaction
from django.contrib.auth.models import User


# Create your models here.
class Person(models.Model):
    FIO = models.CharField(verbose_name="ФИО", max_length=255, db_index=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", db_index=True, blank=True, null=True)
    def __str__(self):
        return self.FIO


class Teacher(Person):
    Position = models.ForeignKey('Position', verbose_name="Должность", db_index=True)
    Zvanie = models.ForeignKey('Zvanie', verbose_name="Звание", db_index=True, blank=True, null=True)
    cathedra = models.ForeignKey('Kafedra', verbose_name="Кафедра", db_index=True)

    def __str__(self):
        return self.FIO


class EduOrg(models.Model):
    name = models.CharField(verbose_name="название института", max_length=200, db_index=True)
    uni = models.ForeignKey('self', verbose_name="Название университета", db_index=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Kafedra(models.Model):
    number = models.IntegerField(verbose_name="номер кафедры", db_index=True, unique=True)
    name = models.CharField(verbose_name="название кафедры", max_length=200, db_index=True)
    institution = models.ForeignKey('EduOrg', verbose_name="Институт", db_index=True)

    def __str__(self):
        return str(self.number) + '-' + self.name


class EduProg(models.Model):
    specialization = models.ForeignKey('Specialization', verbose_name="Специализация", db_index=True)
    profile = models.ForeignKey('Profile', verbose_name="Профиль", db_index=True)
    year = models.ForeignKey('Year', verbose_name="Год", db_index=True)
    cathedra = models.ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True)

    def __str__(self):
        return self.specialization.name


class Group(models.Model):
    Name = models.CharField(verbose_name="название группы", max_length=200, db_index=True)
    beginyear = models.ForeignKey('Year', verbose_name="Год начала обучения", db_index=True, blank=True, null=True)
    cathedra = models.ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, blank=True, null=True)
    program = models.ForeignKey(EduProg, verbose_name="Программа", db_index=True, blank=True, null=True)

    class Meta:
        verbose_name = 'группа'
        verbose_name_plural = 'группы'
        ordering = ['Name']

    def __str__(self):
        return self.Name

    @property
    def year(self):
        now = datetime.now()
        t = int(now.year) - self.beginyear.year + 1
        return (t//2 + t%2)

    def get_semesters(self, edu_period):
        try:
            autumn_semester = Semestr.objects.get( name=str(( edu_period.beginyear.year - self.beginyear.year ) * 2 + 1))
            spring_semester = Semestr.objects.get( name=str(( edu_period.beginyear.year - self.beginyear.year ) * 2 + 2))
        except Exception as e:
            raise Exception('Система не настроена!! Нет соответствущих учебному году семестров!!')
        return (autumn_semester.id, spring_semester.id)

    def add_discpline(self, discpline):
        course = Course()
        course.group = self
        course.discipline_detail = discpline
        course.lecturer = None
        course.save()

    def fill_group_disciplines(self, edu_period=None):
        if self.program is None:
            raise Exception('Для группы не определена программа обучения!! Исправьте!!')
        if edu_period is None:
            try:
                edu_period = EduPeriod.objects.get(active=True)
            except Exception as e:
                raise Exception('Система не настроена! Вы не определили активный учебный год или их несколько!!!')
        semesters = self.get_semesters(edu_period)
        disciplines_details = DisciplineDetails.objects.filter(discipline__program__id=self.program.id, semestr__id__in=semesters)
        with transaction.atomic():
            for discipline_detail in disciplines_details:
                self.add_discpline(discipline_detail)


class Specialization(models.Model):
    name = models.CharField(verbose_name="название специализации", max_length=200, db_index=True,
                    )
    briefname = models.CharField(verbose_name="короткое имя специализации", max_length=50, db_index=True, blank=True,
                                 null=True)
    code = models.CharField(verbose_name="код специализации", max_length=100, db_index=True, unique=True)
    qual = models.ForeignKey('Qual', verbose_name="Квалификация", db_index=True)
    level = models.ForeignKey('Level', verbose_name="Уровень", db_index=True, blank=True, null=True)

    def __str__(self):
        return self.name


'''class DisciplineTeacher(models.Model):
    discipline = models.ForeignKey(Discipline, verbose_name="Дисциплина", db_index=True)
    teacher = models.ForeignKey(Teacher, verbose_name="Преподаватель", db_index=True)
    eduperiod = models.ForeignKey(EduPeriod, verbose_name="Период")
'''

class Discipline(models.Model):
    Name = models.CharField(verbose_name="название дисциплины", max_length=200, db_index=True)
    code = models.CharField(verbose_name="код дисциплины", max_length=200, db_index=True)
    program = models.ForeignKey(EduProg, verbose_name="Программа образования", db_index=True)

    def __str__(self):
            return self.Name


class DisciplineDetails(models.Model):
    discipline = models.ForeignKey(Discipline, verbose_name="Дисциплина", db_index=True)
    Credit = models.IntegerField(verbose_name="ЗЕТ", db_index=True, blank=True, null=True)
    Lecture = models.IntegerField(verbose_name="количество лекции", db_index=True, blank=True, null=True)
    Practice = models.IntegerField(verbose_name="количество практики", db_index=True, blank=True, null=True)
    Lab = models.IntegerField(verbose_name="количество лабораторных работ", db_index=True, blank=True, null=True)
    KSR = models.IntegerField(verbose_name="количество контрольно-самостоятельных работ", db_index=True, blank=True, null=True)
    SRS = models.IntegerField(verbose_name="количество срс", db_index=True, blank=True, null=True)
    semestr = models.ForeignKey('Semestr', verbose_name="Семестр", db_index=True)

    class Meta:
        unique_together=(('discipline', 'semestr'),)

    def __str__(self):
            return self.discipline.Name + ' - ' + self.semestr.name + ' семестр'

    @property
    def total_hours(self):
        return self.Lecture + self.Practice + self.Lab + self.KSR + self.SRS

    @property
    def controls(self):
        return ', '.join(list(self.control_set.all().values_list('controltype__name', flat=True)))


class Control(models.Model):
    discipline_detail = models.ForeignKey('DisciplineDetails',verbose_name="Дисциплина", db_index=True, blank=True, null=True)
    controltype = models.ForeignKey('ControlType', verbose_name="Тип контроля", db_index=True, blank=True, null=True)
    control_hours = models.IntegerField(verbose_name="Кол-во часов", default=0, db_index=True)

    class Meta:
        unique_together=(('discipline_detail','controltype'),)

    def __str__(self):
            return self.controltype.name + ' - ' + self.discipline_detail.discipline.Name + ' - ' \
                   + self.discipline_detail.semestr.name + ' семестр'


class Year(models.Model):
    year = models.IntegerField(verbose_name="год поступления", db_index=True, unique=True)

    def __str__(self):
            return str(self.year)


class Position(models.Model):
    name = models.CharField(verbose_name="Позиция", db_index=True, max_length=255, unique=True)

    def __str__(self):
        return self.name


class Zvanie(models.Model):
    name = models.CharField(verbose_name="Звание", db_index=True, max_length=255, unique=True)

    def __str__(self):
            return self.name


class Level(models.Model):
    name = models.CharField(verbose_name="Уровень", db_index=True, max_length=255, unique=True)

    def __str__(self):
            return self.name


class Profile(models.Model):
    spec = models.ForeignKey('Specialization', verbose_name="Специализация", db_index=True)
    name = models.CharField(verbose_name="Профиль", db_index=True, max_length=255, unique=True)

    def __str__(self):
            return self.spec.name + self.name


class Qual(models.Model):
    name = models.CharField(verbose_name="Квалификация", db_index=True, max_length=255, unique=True)

    def __str__(self):
            return self.name


class ControlType(models.Model):
    name = models.CharField(verbose_name="Тип контроля", db_index=True, max_length=255, unique=True)

    def __str__(self):
            return self.name


class Semestr(models.Model):
    name = models.CharField(verbose_name="Семестр", db_index=True, max_length=255, unique=True)

    def __str__(self):
            return self.name


class Mark(models.Model):
    name = models.CharField(verbose_name="Оценка", db_index=True, max_length=255, unique=True)

    def __str__(self):
            return self.name


class MarkSymbol(models.Model):
    name = models.CharField(verbose_name="Буквенный эквивалент оценки", db_index=True, blank=True, null=True,
                            max_length=255, unique=True)

    def __str__(self):
            return self.name


class CheckPoint(models.Model):
    name = models.CharField(verbose_name="Срез", db_index=True, max_length=255, unique=True)

    def __str__(self):
            return self.name


class EduPeriod(models.Model):
    beginyear = models.ForeignKey(Year, verbose_name="Начало учебного года", related_name='eduperiod_beginyear')
    endyear = models.ForeignKey(Year, verbose_name="Конец учебного года", related_name='eduperiod_endyear')
    active = models.BooleanField(verbose_name="Статус", db_index=True)

    def __str__(self):
            return str(self.beginyear.year) + '-' + str(self.endyear.year)


class Student(Person):
    StudentID = models.CharField(verbose_name="Номер зачетной книжки", db_index=True,
                                 max_length=255)

    def __str__(self):
        return self.FIO


class GroupList(models.Model):
    active = models.BooleanField(verbose_name="Статус", db_index=True)
    group = models.ForeignKey('Group', verbose_name="Группа", db_index=True)
    student = models.ForeignKey('Student', verbose_name="Студент", db_index=True)

    def __str__(self):
            return self.student.FIO + ' - ' + self.group.Name


class Course(models.Model):
    group = models.ForeignKey(Group, verbose_name="Группа", db_index=True)
    discipline_detail = models.ForeignKey(DisciplineDetails, verbose_name="Дисциплина", db_index=True)
    lecturer = models.ForeignKey(Teacher, verbose_name="Преподаватель", db_index=True, blank=True, null=True)

    def __str__(self):
        return self.group.Name + ':' + self.discipline_detail.discipline.Name


class CourseMaxPoints(models.Model):
    course = models.ForeignKey(Course, verbose_name="Курс", db_index=True)
    checkpoint = models.ForeignKey(CheckPoint, verbose_name="Срез", db_index=True)
    maxpoint = models.DecimalField(verbose_name="Максимальные баллы", max_digits=5, decimal_places=2)

    def __str__(self):
        return self.course.discipline_detail.discipline.Name + '-' + self.checkpoint.name + ': ' + str(self.maxpoint)


class BRSpoints(models.Model):
    student = models.ForeignKey(Student, db_index=True)
    checkpoint = models.ForeignKey(CheckPoint, db_index=True)
    points = models.FloatField(verbose_name="Баллы", db_index=True, max_length=255)
    course = models.ForeignKey(Course, db_index=True)

    class Meta:
        permissions = (
            ('can_view_scores', 'Can view students brs scores'),
        )

    def __str__(self):
        return self.student.FIO + ' - ' + self.course.discipline_detail.discipline.Name


class Exam(models.Model):
    examDate = models.CharField(verbose_name="Дата экзамена", db_index=True, max_length=255)
    course = models.ForeignKey(Course, db_index=True)
    controlType = models.ForeignKey(ControlType, db_index=True)
    prev_exam = models.ForeignKey('self', verbose_name="Предыдущий экзамен", blank=True, null=True )

    def __str__(self):
        return self.course.discipline_detail.discipline.Name + '"' + self.examDate + '"'


class ExamMarks(models.Model):
    exam = models.ForeignKey(Exam, db_index=True)
    student = models.ForeignKey(Student, db_index=True)
    inPoints = models.FloatField(verbose_name="Баллы за срез", max_length=255)
    additional_points = models.FloatField(verbose_name="Баллы за отработку", blank=True, null=True, max_length=255)
    examPoints = models.FloatField(verbose_name="Баллы за экзамен", blank=True, null=True, max_length=255)
    mark = models.ForeignKey(Mark, db_index=True)
    markSymbol = models.ForeignKey(MarkSymbol, db_index=True, blank=True, null=True)

    def __str__(self):
        return self.student.FIO + ' - ' + self.exam.course.discipline_detail.discipline.Name + ' - ' + self.mark.name


class Synch(models.Model):
    date = models.DateTimeField()
    finished = models.BooleanField()

    def __str__(self):
        return 'None'
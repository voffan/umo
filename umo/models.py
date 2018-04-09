from django.db import models
from django.core.urlresolvers import reverse


# Create your models here.
class Person(models.Model):
    FIO = models.CharField(verbose_name="ФИО", max_length=255, db_index=True, blank=False, null=False)

    def __str__(self):
        return self.FIO


class Teacher(Person):
    Position = models.ForeignKey('Position', verbose_name="Должность", db_index=True, blank=False, null=False)
    Zvanie = models.ForeignKey('Zvanie', verbose_name="Звание", db_index=True, blank=True, null=True)
    cathedra = models.ForeignKey('Kafedra', verbose_name="Кафедра", db_index=True)

    def __str__(self):
        return self.FIO


class EduOrg(models.Model):
    name = models.CharField(verbose_name="название института", max_length=200, db_index=True, blank=False, null=False)
    uni = models.ForeignKey('self', verbose_name="Название университета", db_index=True, null=True, blank=True)

    def __str__(self):
        return self.name


class Kafedra(models.Model):
    number = models.IntegerField(verbose_name="номер кафедры", db_index=True, blank=False, null=False)
    name = models.CharField(verbose_name="название кафедры", max_length=200, db_index=True, blank=False, null=False)
    institution = models.ForeignKey('EduOrg', verbose_name="Институт", db_index=True, blank=False, null=False)

    def __str__(self):
        return self.name


class EduProg(models.Model):
    specialization = models.ForeignKey('Specialization', verbose_name="Специализация", db_index=True, blank=False,
                                       null=False)
    profile = models.ForeignKey('Profile', verbose_name="Профиль", db_index=True, blank=False, null=False)
    year = models.ForeignKey('Year', verbose_name="Год", db_index=True, blank=False, null=False)
    cathedra = models.ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, blank=False, null=False)

    def __str__(self):
        return self.specialization.name


class Group(models.Model):
    Name = models.CharField(verbose_name="название группы", max_length=200, db_index=True, blank=False, null=False)
    beginyear = models.ForeignKey('Year', verbose_name="Год начала обучения", db_index=True, blank=False, null=False)
    cathedra = models.ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, blank=False, null=False)
    program = models.ForeignKey(EduProg, verbose_name="Программа", db_index=True, blank=False, null=False)

    def __str__(self):
        return self.Name


class Specialization(models.Model):
    name = models.CharField(verbose_name="название специализации", max_length=200, db_index=True, blank=False,
                            null=False)
    briefname = models.CharField(verbose_name="короткое имя специализации", max_length=200, db_index=True, blank=False,
                                 null=False)
    code = models.IntegerField(verbose_name="код специализации", db_index=True, blank=False, null=False)
    qual = models.ForeignKey('Qual', verbose_name="Квалификация", db_index=True, blank=False, null=False)
    level = models.ForeignKey('Level', verbose_name="Уровень", db_index=True, blank=False, null=False)

    def __str__(self):
        return self.name


class Discipline(models.Model):
    Name = models.CharField(verbose_name="название дисциплины", max_length=200, db_index=True, blank=False, null=False)
    code = models.IntegerField(verbose_name="код дисциплины", db_index=True, blank=False, null=False)
    program = models.ForeignKey(EduProg, verbose_name="Программа образования", db_index=True, blank=False, null=False)
    lecturer = models.ForeignKey(Teacher, verbose_name="Преподаватель", db_index=True, blank=False, null=False)
    control = models.ForeignKey('Control', verbose_name="Тип контроля", db_index=True, blank=False, null=False)

    def get_absolute_url(self):
        return reverse('disciplines:detail', kwargs={'pk': self.pk})

    def __str__(self):
            return self.Name


class DisciplineDetails(models.Model):
    Credit = models.IntegerField(verbose_name="количество часов", db_index=True, blank=False, null=False)
    Lecture = models.IntegerField(verbose_name="количество лекции", db_index=True, blank=False, null=False)
    Practice = models.IntegerField(verbose_name="количество практики", db_index=True, blank=False, null=False)
    Lab = models.IntegerField(verbose_name="количество лабораторных работ", db_index=True, blank=False, null=False)
    KSR = models.IntegerField(verbose_name="количество контрольно-самостоятельных работ", db_index=True, blank=False,
                              null=False)
    SRS = models.IntegerField(verbose_name="количество срс", db_index=True, blank=False, null=False)
    semestr = models.ForeignKey('Semestr', verbose_name="Семестр", db_index=True, blank=False, null=False)
    subject = models.ForeignKey(Discipline, verbose_name="Предмет", db_index=True, blank=False, null=False)

    def __str__(self):
            return self.subject.Name


class Control(models.Model):
    controltype = models.CharField(verbose_name="тип контроля", max_length=100, db_index=True, blank=False, null=False)
    hours = models.IntegerField(verbose_name="кол-во часов", db_index=True, null=False)

    def __str__(self):
            return self.controltype


class Year(models.Model):
    year = models.CharField(verbose_name="год поступления", max_length=4, db_index=True, blank=False, null=False)

    def __str__(self):
            return self.year


class Position(models.Model):
    name = models.CharField(verbose_name="Позиция", db_index=True, blank=False, null=False, max_length=255)

    def __str__(self):
        return self.name


class Zvanie(models.Model):
    name = models.CharField(verbose_name="Звание", db_index=True, blank=False, null=False, max_length=255)

    def __str__(self):
            return self.name


class Level(models.Model):
    name = models.CharField(verbose_name="Уровень", db_index=True, blank=False, null=False, max_length=255)

    def __str__(self):
            return self.name


class Profile(models.Model):
    name = models.CharField(verbose_name="Профиль", db_index=True, blank=False, null=False, max_length=255)

    def __str__(self):
            return self.name


class Qual(models.Model):
    name = models.CharField(verbose_name="Квалификация", db_index=True, blank=False, null=False, max_length=255)

    def __str__(self):
            return self.name


class ControlType(models.Model):
    name = models.CharField(verbose_name="Тип контроля", db_index=True, blank=False, null=False, max_length=255)

    def __str__(self):
            return self.name


class Semestr(models.Model):
    name = models.CharField(verbose_name="Семестр", db_index=True, blank=False, null=False, max_length=255)

    def __str__(self):
            return self.name


class Mark(models.Model):
    name = models.CharField(verbose_name="Оценка", db_index=True, blank=False, null=False, max_length=255)

    def __str__(self):
            return self.name


class MarkSymbol(models.Model):
    name = models.CharField(verbose_name="Буквенный эквивалент оценки", db_index=True, blank=False, null=False,
                            max_length=255)

    def __str__(self):
            return self.name


class CheckPoint(models.Model):
    name = models.CharField(verbose_name="Срез", db_index=True, blank=False, null=False, max_length=255)

    def __str__(self):
            return self.name


class EduPeriod(models.Model):
    beginyear = models.IntegerField(verbose_name="Начало учебного года", db_index=True, blank=False, null=False)
    endyear = models.IntegerField(verbose_name="Конец учебного года", db_index=True, blank=False, null=False)
    active = models.BooleanField(verbose_name="Статус", db_index=True, blank=False, null=False)

    def __str__(self):
            return self.beginyear + '-' + self.endyear


class Student(Person):
    StudentID = models.CharField(verbose_name="Номер зачетной книжки", db_index=True, blank=False, null=False,
                                 max_length=255)

    def __str__(self):
        return self.FIO


class GroupList(models.Model):
    active = models.BooleanField(verbose_name="Статус", db_index=True, blank=False, null=False)
    group = models.ForeignKey('Group', verbose_name="Группа", db_index=True, blank=False, null=False)
    student = models.ForeignKey('Student', verbose_name="Студент", db_index=True, blank=False, null=False)

    def __str__(self):
            return self.student.FIO + ' - ' + self.group.Name


class BRS(models.Model):
    discipline = models.ForeignKey(Discipline, db_index=True, blank=False, null=False)
    semester = models.ForeignKey(Semestr, db_index=True, blank=False, null=False)
    eduperiod = models.ForeignKey(EduPeriod, db_index=True, blank=False, null=False)

    def __str__(self):
            return self.discipline.Name


class BRSpoints(models.Model):
    student = models.ForeignKey(Student, db_index=True, blank=False, null=False)
    CheckPoint = models.ForeignKey(CheckPoint, db_index=True, blank=False, null=False)
    points = models.FloatField(verbose_name="Баллы", db_index=True, blank=False, null=False, max_length=255)
    brs = models.ForeignKey(BRS, db_index=True, blank=False, null=False)

    def __str__(self):
            return self.student.FIO + ' - ' + self.brs.discipline.Name


class Exam(models.Model):
    examDate = models.DateField(verbose_name="Дата экзамена", db_index=True, blank=False, null=False)
    discipline = models.ForeignKey(Discipline, db_index=True, blank=False, null=False)
    controlType = models.ForeignKey(ControlType, db_index=True, blank=False, null=False)
    semestr = models.ForeignKey(Semestr, db_index=True, blank=False, null=False)
    eduperiod = models.ForeignKey(EduPeriod, db_index=True, blank=False, null=False)

    def __str__(self):
            return self.discipline.Name + '"' + self.examDate + '"'


class ExamMarks(models.Model):
    student = models.ForeignKey(Student, db_index=True, blank=False, null=False)
    inPoints = models.FloatField(verbose_name="Баллы за срез", db_index=True, blank=False, null=False, max_length=255)
    examPoints = models.FloatField(verbose_name="Баллы за экзамен", db_index=True, blank=False, null=False,
                                   max_length=255)
    mark = models.ForeignKey(Mark, db_index=True, blank=False, null=False)
    markSymbol = models.ForeignKey(MarkSymbol, db_index=True, blank=False, null=False)
    exam = models.ForeignKey(Exam, db_index=True, blank=False, null=False)

    def __str__(self):
        return self.student.FIO + ' - ' + self.exam.discipline.Name

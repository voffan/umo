from django.db import models

# Create your models here.
class Person(models.Model):
    FIO = models.CharField(verbose_name="ФИО", max_length=255, db_index=True, blank=False, null=False)

class Teacher(Person):
    Position = models.ForeignKey('Position', db_index=True, blank=False, null=False)
    Zvanie = models.ForeignKey('Zvanie', db_index=True, blank=False, null=False)
    cathedra = models.ForeignKey('Kafedra', db_index=True, null=True)


class EduOrg(models.Model):
    name = models.CharField(verbose_name="названия института", max_length=200, db_index=True, blank=False, null=False)
    uni = models.ForeignKey('self', db_index=True, null=True, blank=True)

class Kafedra(models.Model):
    number = models.IntegerField(verbose_name="номер кафедры", db_index=True, blank=False, null=False)
    name = models.CharField(verbose_name="названия кафедры", max_length=200, db_index=True, blank=False, null=False)
    institution = models.ForeignKey('EduOrg', db_index=True, blank=False, null=False)


class EduProg(models.Model):
    specialization = models.ForeignKey('Specialization', db_index=True, blank=False, null=False)
    profile = models.ForeignKey('Profile', db_index=True, blank=False, null=False)
    year = models.ForeignKey('Year', db_index=True,blank=False, null=False)
    cathedra = models.ForeignKey(Kafedra, db_index=True, blank=False, null=False)

class Group(models.Model):
    Name = models.CharField(verbose_name="названия группы", max_length=200, db_index=True, blank=False, null=False)
    beginyear = models.ForeignKey('Year', db_index=True, blank=False, null=False)
    cathedra = models.ForeignKey(Kafedra,db_index=True, blank=False, null=False)
    program = models.ForeignKey(EduProg, db_index=True, blank=False, null=False)

class Specialization(models.Model):
    name = models.CharField(verbose_name="названия специализации", max_length=200, db_index=True, blank=False, null=False)
    briefname = models.CharField(verbose_name="короткое имя специализации", max_length=200, db_index=True, blank=False, null=False)
    code = models.IntegerField(verbose_name="код специализации", db_index=True, blank=False, null=False)
    qual = models.ForeignKey('Qual', db_index=True, blank=False, null=False)
    level = models.ForeignKey('Level', db_index=True, blank=False, null=False)

class Discipline(models.Model):
    Name = models.CharField(verbose_name="названия дисциплины", max_length=200, db_index=True, blank=False, null=False)
    code = models.IntegerField(verbose_name="код дисциплины", db_index=True, blank=False, null=False)
    program = models.ForeignKey(EduProg, db_index=True, blank=False, null=False)
    lecturer = models.ForeignKey(Teacher, db_index=True, blank=False, null=False)
    control = models.ForeignKey('Control', db_index=True, blank=False, null=False)

class DisciplineDetails(models.Model):
    Credit = models.IntegerField(verbose_name="количество часов", db_index=True, blank=False, null=False)
    Lecture = models.IntegerField(verbose_name="количество лекции", db_index=True, blank=False, null=False)
    Practice = models.IntegerField(verbose_name="количество практики", db_index=True, blank=False, null=False)
    Lab = models.IntegerField(verbose_name="количество лабораторных работ", db_index=True, blank=False, null=False)
    KSR = models.IntegerField(verbose_name="количество контрольно-самостоятельных работ", db_index=True, blank=False, null=False)
    SRS = models.IntegerField(verbose_name="количество срс", db_index=True, blank=False, null=False)
    semestr = models.ForeignKey('Semestr', db_index=True, blank=False, null=False)
    subject = models.ForeignKey(Discipline, db_index=True, blank=False, null=False)

class Control(models.Model):
    controltype = models.CharField(verbose_name="тип контроля", max_length=100, db_index=True, blank=False, null=False)
    hours = models.IntegerField(verbose_name="часы", db_index=True, null=False)

class Year(models.Model):
    receipts = models.DateTimeField(verbose_name="год поступления", db_index=True, blank=False, null=False)

class Position(models.Model):
    name = models.CharField(verbose_name="Позиция", db_index=True, blank=False, null=False, max_length=255)

class Zvanie(models.Model):
    name = models.CharField(verbose_name="Звание", db_index=True, blank=False, null=False, max_length=255)

class Level(models.Model):
    name = models.CharField(verbose_name="Уровень", db_index=True, blank=False, null=False, max_length=255)

class Profile(models.Model):
    name = models.CharField(verbose_name="Профиль", db_index=True, blank=False, null=False, max_length=255)

class Qual(models.Model):
    name = models.CharField(verbose_name="Квалификация", db_index=True, blank=False, null=False, max_length=255)

class ControlType(models.Model):
    name = models.CharField(verbose_name="Тип контроля", db_index=True, blank=False, null=False, max_length=255)

class Semestr(models.Model):
    name = models.IntegerField(verbose_name="Семестр", db_index=True, blank=False, null=False)

class Mark(models.Model):
    name = models.CharField(verbose_name="Оценка", db_index=True, blank=False, null=False, max_length=255)

class MarkSymbol(models.Model):
    name = models.CharField(verbose_name="Буквенный эквивалент оценки", db_index=True, blank=False, null=False, max_length=255)

class CheckPoint(models.Model):
    name = models.CharField(verbose_name="Срез", db_index=True, blank=False, null=False, max_length=255)

class EduPeriod(models.Model):
    beginyear = models.IntegerField(verbose_name="Начало учебного года", db_index=True, blank=False, null=False)
    endyear = models.IntegerField(verbose_name="Конец учебного года", db_index=True, blank=False, null=False)
    active = models.BooleanField(verbose_name="Статус", db_index=True, blank=False, null=False)

class Student(models.Model):
    StudentID = models.CharField(verbose_name="ID Студента", db_index=True, blank=False, null=False, max_length=255)

class GroupList(models.Model):
    active = models.BooleanField(verbose_name="Статус", db_index=True, blank=False, null=False)
    group = models.ForeignKey('Group', db_index=True, blank=False, null=False)
    student = models.ForeignKey('Student', db_index=True, blank=False, null=False)

class BRS(models.Model):
    discipline = models.ForeignKey(Discipline, db_index=True, blank=False, null=False)
    semester = models.ForeignKey(Semestr, db_index=True, blank=False, null=False)
    eduperiod = models.ForeignKey(EduPeriod, db_index=True, blank=False, null=False)


class BRSpoints(models.Model):
    student = models.ForeignKey(Student, db_index=True, blank=False, null=False)
    CheckPoint = models.ForeignKey(CheckPoint, db_index=True, blank=False, null=False)
    points = models.FloatField(verbose_name="Баллы", db_index=True, blank=False, null=False, max_length=255)
    brs = models.ForeignKey(BRS, db_index=True, blank=False, null=False)

class Exam(models.Model):
    examDate = models.DateField(verbose_name="Дата экзамена", db_index=True, blank=False, null=False)
    discipline = models.ForeignKey(Discipline, db_index=True, blank=False, null=False)
    controlType = models.ForeignKey(ControlType, db_index=True, blank=False, null=False)
    semestr = models.ForeignKey(Semestr, db_index=True, blank=False, null=False)
    eduperiod = models.ForeignKey(EduPeriod, db_index=True, blank=False, null=False)

class ExamMarks(models.Model):
    student = models.ForeignKey(Student, db_index=True, blank=False, null=False)
    inPoints = models.FloatField(verbose_name="Баллы за срез", db_index=True, blank=False, null=False, max_length=255)
    examPoints = models.FloatField(verbose_name="Баллы за экзамен", db_index=True, blank=False, null=False, max_length=255)
    mark = models.ForeignKey(Mark, db_index=True, blank=False, null=False)
    markSymbol = models.ForeignKey(MarkSymbol, db_index=True, blank=False, null=False)
    exam = models.ForeignKey(Exam, db_index=True, blank=False, null=False)
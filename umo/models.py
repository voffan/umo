from django.db import models

# Create your models here.
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

class Group(models.Model):
    Name = models.CharField(verbose_name="Название группы", db_index=True, blank=False, null=False, max_length=255)
    beginyear = models.IntegerField(verbose_name="Начало учебного года", db_index=True, blank=False, null=False)

class Student(models.Model):
    StudentID = models.CharField(verbose_name="ID Студента", db_index=True, blank=False, null=False, max_length=255)

class GroupList(models.Model):
    active = models.BooleanField(verbose_name="Статус", db_index=True, blank=False, null=False)

class BRS(models.Model):
    discipline = models.ForeignKey(Discipline, db_index=True, blank=False, null=False)
    semester = models.ForeignKey(Semestr, db_index=True, blank=False, null=False)
    eduperiod = models.ForeignKey(EduPeriod, db_index=True, blank=False, null=False)

class BRSpoints(models.Model):
    student = models.ForeignKey(Student, db_index=True, blank=False, null=False)
    CheckPoint = models.ForeignKey(CheckPoint, db_index=True, blank=False, null=False)
    points = models.FloatField(verbose_name="Баллы", db_index=True, blank=False, null=False, max_length=255)

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










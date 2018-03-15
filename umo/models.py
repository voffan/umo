from django.db import models

# Create your models here.
class Person(models.Model):
    FIO = models.CharField(verbose_name="ФИО", max_length=255, db_index=True, blank=False, null=False)

class Teacher(Person):
    position = models.CharField(verbose_name="должность", max_length=10, db_index=True, blank=False, null=False)
    zvanie = models.CharField(verbose_name="звание", max_length=10, db_index=True, blank=False, null=False)
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
    profile = models.CharField(verbose_name="профиль", max_length=100, db_index=True, blank=False, null=False)
    year = models.ForeignKey('Year', db_index=True,blank=False, null=False)
    cathedra = models.ForeignKey(Kafedra, db_index=True, blank=False, null=False)

class Group(models.Model):
    name = models.CharField(verbose_name="названия группы", max_length=200, db_index=True, blank=False, null=False)
    year = models.ForeignKey('Year', db_index=True, blank=False, null=False)
    cathedra = models.ForeignKey(Kafedra,db_index=True, blank=False, null=False)
    program = models.ForeignKey(EduProg, db_index=True, blank=False, null=False)

class Specialization(models.Model):
    name = models.CharField(verbose_name="названия специализации", max_length=200, db_index=True, blank=False, null=False)
    code = models.IntegerField(verbose_name="код специализации", db_index=True, blank=False, null=False)
    qual = models.CharField(verbose_name="квалификация специализации", max_length=200, db_index=True, blank=False, null=False)
    level = models.CharField(verbose_name="уровень специализации", max_length=10, db_index=True, blank=False, null=False)

class Discipline(models.Model):
    name = models.CharField(verbose_name="названия дисциплины", max_length=200, db_index=True, blank=False, null=False)
    code = models.IntegerField(verbose_name="код дисциплины", db_index=True, blank=False, null=False)
    program = models.ForeignKey(EduProg, db_index=True, blank=False, null=False)
    lecturer = models.ForeignKey(Teacher, db_index=True, blank=False, null=False)
    control = models.ForeignKey('Control', db_index=True, blank=False, null=False)

class DisciplineDetails(models.Model):
    credit = models.IntegerField(verbose_name="количество часов", db_index=True, blank=False, null=False)
    lecture = models.IntegerField(verbose_name="количество лекции", db_index=True, blank=False, null=False)
    practice = models.IntegerField(verbose_name="количество практики", db_index=True, blank=False, null=False)
    lab = models.IntegerField(verbose_name="количество лабораторных работ", db_index=True, blank=False, null=False)
    ksr = models.IntegerField(verbose_name="количество контрольно-самостоятельных работ", db_index=True, blank=False, null=False)
    srs = models.IntegerField(verbose_name="количество срс", db_index=True, blank=False, null=False)
    semestr = models.IntegerField(verbose_name="семестр", db_index=True, blank=False, null=False)
    subject = models.ForeignKey(Discipline, db_index=True, blank=False, null=False)

class Control(models.Model):
    controltype = models.CharField(verbose_name="тип контроля", max_length=100, db_index=True, blank=False, null=False)
    hours = models.IntegerField(verbose_name="часы", db_index=True, null=False)

class Year(models.Model):
    receipts = models.DateTimeField(verbose_name="год поступления", db_index=True, blank=False, null=False)





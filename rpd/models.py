from django.db import models
from django.db.models import Model, ForeignKey, CASCADE, IntegerField, CharField
from umo.models import Semester, Discipline
# Create your models here.
#WorkType
lecture = 1
labs = 2
SRS = 3
test = 4
practice = 5
#Language
russian = 1
english = 2
#CriteriaType
admission = 1
presentation = 2
#SRSType
SRS = 1
labs = 2
#Level
hight = 1
base = 2
minimal = 3
complete = 4
not_complete = 5
#Marks
0 = 0
1 = 1
2 = 2
3 = 3
4 = 4
5 = 5
6 = 6
7 = 7
8 = 8
9 = 9


#Вспомогательные классы
WorkType = (
    (lecture, 'Лекция'),
    (labs, 'Лабораторная'),
    (SRS, 'Самостоятельная'),
    (test, 'Контрольная'),
    (practice, 'Практическая'),
)

Language = (
    (russian, 'Русский язык'),
    (english, 'Английский язык'),
)

CriteriaType = (
    (admission, 'Допуск'),
    (presentation, 'Недопуск'),
)

SRSType = (
    (SRS,'Самостоятельная'),
    (labs, 'Лабораторная')
)

Level = (
    (hight,'Высокий'),
    (base, 'Базовый'),
    (minimal,'Минимальный'),
    (complete,'Освоено'),
    (not_complete,'Неосвоено'),
)

Marks = (
    (0,'0')
)


#Классы UMO
class Discipline(Model):
    discipline_name = CharField(verbose_name="Название дисциплины", db_index=True, default=1)
    discipline_code = IntegerField(verbose_name="Код дисциплины", db_index=True, default=1)


class DisciplineDetail(Model):
   pass


class Competency(Model):
    pass

class CompetencyType(Model):
    pass

class CompetencyIndicator(Model):
    pass


class EduProgram(Model):
    name = CharField(verbose_name="Название", db_index=True, default=1)
    specialization = CharField(verbose_name="Специализация", db_index=True, default=1)
    profile = CharField(verbose_name="Направление", db_index=True, default=1)
    year = CharField(verbose_name="Год обучения", db_index=True, default=1)
    cathedra = CharField(verbose_name="Кафедра", db_index=True, default=1)


class Control(Model):
    pass



#Классы вне UMO
class RPDDiscipline(Discipline):
    pass

class Basement(Model):
    pass


class DisciplineResult(Model):
    pass

class RPDDisciplineContent(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    theme = CharField(verbose_name="Тема", db_index=True, default=1)
    content = CharField(verbose_name="Содержимое", db_index=True, default=1)
    #ситэтэ суох

class SRS_Description(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    theme = #
    SRS_type = IntegerField(verbose_name="Тип самостоятельной", choices=SRSType, db_index=True, default=1)
    class_type = #
    hours = IntegerField(verbose_name="Часы",  db_index=True, default=200)
    control = CharField(verbose_name="Контроль", db_index=True, default=1)


class DisciplineRating(Model):
    semester = ForeignKey(Semester, verbose_name="Семестр", db_index=True, on_delete=CASCADE)
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    work_type = IntegerField(verbose_name="Тип занятия", choices=WorkType, db_index=True, default=1)
    max_points = IntegerField(verbose_name="Макс.балл",  db_index=True, default=100)
    min_points = IntegerField(verbose_name="Мин.балл",  db_index=True, default=1)


class MarkScale(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    skill = #
    level = IntegerField(verbose_name="Уровень освоения", choices=Level, db_index=True, default=1)
    criteria = CharField(verbose_name="Критерии", db_index=True, default=1)
    mark = IntegerField(verbose_name="Оценка", choices=Marks, db_index=True, default=1)


class FOS(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    skill = #
    theme = CharField(verbose_name="Тема", db_index=True, default=1)
    sample = CharField(verbose_name="Образец", db_index=True, default=1)


class Bibliography(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    pass

class CourseWorkRating(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    criteria_type = IntegerField(verbose_name="Тип критерий", choices=CriteriaType, db_index=True, default=1)
    criteria = CharField(verbose_name="Критерии", db_index=True, default=1)
    max_points = IntegerField(verbose_name="Макс.балл", db_index=True, default=100)
    min_points = IntegerField(verbose_name="Мин.балл", db_index=True, default=1)

class ClassType(Model): #подкласс?
    SRS_type = IntegerField(verbose_name="Тип самостоятельной", choices=SRSType, db_index=True, default=1)
    name = CharField(verbose_name="Название", db_index=True, default=1)

class ELibrary(Model): #подкласс?
    name = CharField(verbose_name="Название", db_index=True, default=1)

class ClassType(Model):  # подкласс?
    main = CharField(verbose_name="Основная литература", db_index=True, default=1)
    addition =CharField(verbose_name="Дополнительная литература", db_index=True, default=1)
    URL = CharField(verbose_name="Ссылка на веб-русурс", db_index=True, default=1)
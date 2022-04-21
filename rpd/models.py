from django.db import models
from django.db.models import Model, ForeignKey, CASCADE, IntegerField, CharField, SET_NULL, TextField, BooleanField
from umo.models import Semester, Discipline, ExamMarks, EduProgram, Kafedra, Control

# Create your models here.
#HourType
lecture = 1
online_lecture = 2
seminar = 3
online_seminar = 4
labs = 5
online_labs = 6
practice = 7
online_practice = 8
KSR = 9
SRS = 10
#Language
russian = 1
english = 2
#RatingType
exam_rating = 1
credit_rating = 2
course_work_rating = 3
presentation_rating = 4
#SRSType
SRS = 1
labs = 2
#Level
hight = 1
base = 2
minimal = 3
complete = 4
not_complete = 5


#Вспомогательные классы

Language = (
    (russian, 'Русский язык'),
    (english, 'Английский язык'),
)

RatingType = (
    (exam_rating, 'Рейтинг дисциплины с экзаменом'),
    (credit_rating, 'Рейтинг дисциплины с зачетом'),
    (course_work_rating, 'Рейтинг курсовой работы'),
    (presentation_rating, 'Рейтинг защиты курсовой'),
)

PracticeType = (
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

HourType = (
    (lecture, 'Лекция'),
    (online_lecture,'Онлайн лекция'),
    (seminar,'Семинар'),
    (online_seminar,'Онлайн семинар'),
    (labs,'Лабораторная'),
    (online_labs,'Онлайн лабораторная'),
    (practice,'Практика'),
    (online_practice,'Онлайн практика'),
    (KSR,'Консультация'),
    (SRS,'Самостоятельная'),
)

#Классы UMO


#class CompetencyType(Model):#подкласс
#    name = CharField(verbose_name="Название", max_length=250, db_index=True, default=1)

#class Competency(Model):
#    edu_program = ForeignKey(EduProgram, verbose_name="Компетенция", db_index=True, on_delete=CASCADE)
#    type = ForeignKey(CompetencyType, verbose_name="Вид компетенции", db_index=True, on_delete=CASCADE)
#    name = CharField(verbose_name="Название", max_length=250, db_index=True, default=1)

#class CompetencyIndicator(Model):
#    competency = ForeignKey(Competency, verbose_name="Компетенция", db_index=True, on_delete=CASCADE)
#    indicator = CharField(verbose_name="Индикаторы",max_length=500, db_index=True, default=1)


#Классы вне UMO
class RPDDiscipline(Discipline):
    goal = CharField(verbose_name="Цель",max_length=500, db_index=True)
    language = IntegerField('Язык', choices=Language, db_index=True, default=1)
    # Далее обдумать
    education_methodology = CharField(verbose_name="Методология обучения",max_length=500, db_index=True)
    methodological_instructions = CharField(verbose_name="Методические указания для обучающихся ",max_length=500, db_index=True)
    scaling_methodology = CharField(verbose_name="???",max_length=500, db_index=True)
    material = CharField(verbose_name="Перечень материально-технической базы",max_length=1000, db_index=True)
    it = CharField(verbose_name="Перечень информационных технологий",max_length=1000, db_index=True)
    software = CharField(verbose_name="Перечень программного обеспечения",max_length=1000, db_index=True)
    iss = CharField(verbose_name="Перечень информационных справочных систем",max_length=1000, db_index=True)

class Basement(Model):
    discipline = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    base = ForeignKey(RPDDiscipline, verbose_name="Базовые знания", db_index=True, on_delete=CASCADE)


class DisciplineResult(Model):
    competency = ForeignKey(Competency, verbose_name="Компетенция", db_index=True, on_delete=CASCADE)
    indicator = ForeignKey(CompetencyIndicator, verbose_name="Индикатор компетенции", db_index=True, on_delete=CASCADE)
    skill = CharField(verbose_name="Планируемые результаты",max_length=500, db_index=True)
    fos = CharField(verbose_name="Оценочные средства",max_length=500, db_index=True)

class RPDDisciplineContent(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    theme = CharField(verbose_name="Тема",max_length=500, db_index=True, default=1)
    content = CharField(verbose_name="Содержимое",max_length=1000, db_index=True, default=1)

class RPDDisciplineContentHours(Model):
    content = ForeignKey(RPDDisciplineContent, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    hours_type = IntegerField('Тип работы', choices=HourType, db_index=True, default=1)
    hours = IntegerField(verbose_name="Кол-во часов",  db_index=True, default=200)


class ClassType(Model): #подкласс
    name = CharField(verbose_name="Название",max_length=250, db_index=True)

class PracticeDescription(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    practice_type = IntegerField('Тип практикума', choices=PracticeType, db_index=True, default=1)
    theme = ForeignKey(RPDDisciplineContent, verbose_name='Тема', db_index=True, on_delete=CASCADE)
    class_type = ForeignKey(ClassType, verbose_name='Вид работы', db_index=True, on_delete=CASCADE)
    hours = IntegerField(verbose_name="Кол-во часов",  db_index=True, default=200)
    control = CharField(verbose_name="Контроль", max_length=300, db_index=True, default=1)

class WorkType(Model): #подкласс
    name = CharField('Наименование типа работы', max_length=250, db_index=True)

class DisciplineRating(Model):
    rating_type = IntegerField('Вид рейтинговой таблицы', choices=RatingType, db_index=True, default=exam_rating)
    semester = ForeignKey(Semester, verbose_name="Семестр", db_index=True, on_delete=CASCADE)
    work_type = ForeignKey(WorkType, verbose_name='Вид работы', db_index=True, on_delete=CASCADE)
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    max_points = IntegerField(verbose_name="Макс.балл",  default=100)
    min_points = IntegerField(verbose_name="Мин.балл",  default=1)


class MarkScale(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    skill = ForeignKey(DisciplineResult, verbose_name='Показатель оценивания', db_index=True, on_delete=CASCADE)
    level = IntegerField(verbose_name="Уровень освоения", choices=Level, db_index=True, default=1)
    criteria = CharField(verbose_name="Критерии",max_length=1000, db_index=True, default=1)
    mark = IntegerField(verbose_name="Оценка", choices=ExamMarks.MARKS, db_index=True, default=1)


class FOS(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    skill = ForeignKey(DisciplineResult, verbose_name='Показатель оценивания', db_index=True, on_delete=CASCADE)
    theme = CharField(verbose_name="Тема", max_length=200, db_index=True, default=1)
    sample = CharField(verbose_name="Образец", max_length=1000, db_index=True, default=1)



class ELibrary(Model): #подкласс
    name = CharField(verbose_name="Название",max_length=100, db_index=True, default=1)


class Bibliography(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    reference = TextField(verbose_name="Библиографическая ссылка")
    elibrary = ForeignKey(ELibrary, verbose_name='Электронная литература', null=True, blank=True, db_index=True, on_delete=SET_NULL)
    URL = CharField(verbose_name="Ссылка на веб-русурс",max_length=500, db_index=True, default=1)
    is_main = BooleanField("Главная литература", default=False)

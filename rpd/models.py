from django.db import models
from django.db.models import Model, ForeignKey, CASCADE, IntegerField, CharField
from umo.models import Semester, Discipline, ExamMarks
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
    control = CharField(verbose_name="Контроль", max_length=300, db_index=True, default=1)

class WorkType(Model):
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
    criteria = CharField(verbose_name="Критерии", db_index=True, default=1)
    mark = IntegerField(verbose_name="Оценка", choices=ExamMarks.MARKS, db_index=True, default=1)


class FOS(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    skill = ForeignKey(DisciplineResult, verbose_name='Показатель оценивания', db_index=True, on_delete=CASCADE)
    theme = CharField(verbose_name="Тема", max_length=200, db_index=True, default=1)
    sample = CharField(verbose_name="Образец", max_length=1000, db_index=True, default=1)


class Bibliography(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)


class ClassType(Model): #подкласс?
    SRS_type = IntegerField(verbose_name="Тип самостоятельной", choices=SRSType, db_index=True, default=1)
    name = CharField(verbose_name="Название", db_index=True, default=1)

class ELibrary(Model): #подкласс?
    name = CharField(verbose_name="Название", db_index=True, default=1)

class ClassType(Model):  # подкласс?
    main = CharField(verbose_name="Основная литература", db_index=True, default=1)
    addition =CharField(verbose_name="Дополнительная литература", db_index=True, default=1)
    URL = CharField(verbose_name="Ссылка на веб-русурс", db_index=True, default=1)
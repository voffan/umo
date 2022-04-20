from django.db import models
from django.db.models import Model, ForeignKey, CASCADE, IntegerField, CharField, SET_NULL
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

Marks = (
    (0,'0')
    (1,'2')
    (3,'3')
    (4,'4')
    (5,'5')
    (6,'6')
    (7,'7')
    (8,'8')
    (9,'9')
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
class Discipline(Model):
    Name = CharField(verbose_name="Название дисциплины", max_length=200, db_index=True)
    code = CharField(verbose_name="Код дисциплины", max_length=200, db_index=True)
    program = ForeignKey('EduProgram', verbose_name="Программа образования", db_index=True, on_delete=CASCADE)

class DisciplineDetails(Model):
    discipline = ForeignKey(Discipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    Credit = IntegerField(verbose_name="ЗЕТ", db_index=True, blank=True, null=True)
    Lecture = IntegerField(verbose_name="Количество лекции", db_index=True, blank=True, null=True)
    Practice = IntegerField(verbose_name="Количество практики", db_index=True, blank=True, null=True)
    Lab = IntegerField(verbose_name="Количество лабораторных работ", db_index=True, blank=True, null=True)
    KSR = IntegerField(verbose_name="Количество контрольно-самостоятельных работ", db_index=True, blank=True, null=True)
    SRS = IntegerField(verbose_name="Количество срс", db_index=True, blank=True, null=True)
    semester = ForeignKey('Semester', verbose_name="Семестр", db_index=True, null=True, on_delete=models.CASCADE)

class EduProgram(Model):
    name = CharField(verbose_name="Имя плана подготовки", db_index=True, max_length=100)
    specialization = ForeignKey('Specialization', verbose_name="Специализация", db_index=True, on_delete=CASCADE)
    profile = ForeignKey('Profile', verbose_name="Профиль", db_index=True, on_delete=CASCADE)
    year = ForeignKey('Year', verbose_name="Год", db_index=True, null=True, on_delete=SET_NULL)
    cathedra = ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, on_delete=CASCADE)

class CompetencyType(Model):#подкласс
    name = CharField(verbose_name="Название", max_length=250, db_index=True, default=1)

class Competency(Model):
    edu_program = ForeignKey(EduProgram, verbose_name="Компетенция", db_index=True, on_delete=CASCADE)
    type = ForeignKey(CompetencyType, verbose_name="Вид компетенции", db_index=True, on_delete=CASCADE)
    name = CharField(verbose_name="Название", max_length=250, db_index=True, default=1)

class CompetencyIndicator(Model):
    competency = ForeignKey(Competency, verbose_name="Компетенция", db_index=True, on_delete=CASCADE)
    indicator = CharField(verbose_name="Индикаторы",max_length=500, db_index=True, default=1)

class Control(Model):
    discipline_detail = ForeignKey('DisciplineDetails', verbose_name="Дисциплина", db_index=True, blank=True, null=True, on_delete=CASCADE)
    control_type = IntegerField('Форма контроля', choices = Control.CONTROL_FORM, blank=True, default=0)
    control_hours = IntegerField(verbose_name="Кол-во часов", default=0, db_index=True)

class Semester(Model):
    name = CharField(verbose_name="Семестр", db_index=True, max_length=255, unique=True)



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

class Practice_Description(Model):
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
    main = CharField(verbose_name="Основная литература",max_length=500, db_index=True, default=1)
    addition = CharField(verbose_name="Дополнительная литература",max_length=500, db_index=True, default=1)
    digital_library = ForeignKey(ELibrary, verbose_name='Электронная литература', db_index=True, on_delete=CASCADE)
    URL = CharField(verbose_name="Ссылка на веб-русурс",max_length=500, db_index=True, default=1)





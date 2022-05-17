from django.db import models
from django.db.models import Model, ForeignKey, CASCADE, IntegerField, CharField, SET_NULL, TextField, BooleanField
from umo.models import Semester, Discipline, ExamMarks, EduProgram, Kafedra, Control, Competency, CompetencyIndicator

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
#PracticeType
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
    education_methodology = TextField(verbose_name="Формы и методы проведения занятий, применяемые учебные технологии")
    methodological_instructions = TextField(verbose_name="Методические указания для обучающихся по освоению дисциплины")
    scaling_methodology = TextField(verbose_name="Методические материалы, определяющие процедуры оценивания")
    fos_methodology = TextField(verbose_name="Примерные контрольные задания (вопросы) для промежуточной аттестации")
    web_resource = TextField(verbose_name="Перечень ресурсов информационно-телекоммуникационной сети Интернет")
    material = TextField(verbose_name="Перечень материально-технической базы")
    it = TextField(verbose_name="Перечень информационных технологий")
    software = TextField(verbose_name="Перечень программного обеспечения")
    iss = TextField(verbose_name="Перечень информационных справочных систем")


class Basement(Model):
    discipline = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", related_name='bases', db_index=True, on_delete=CASCADE)
    base = ForeignKey(RPDDiscipline, verbose_name="Базовые знания", db_index=True, on_delete=CASCADE)


class DisciplineResult(Model):
    competency = ForeignKey(Competency, verbose_name="Компетенция", db_index=True, on_delete=CASCADE)
    indicator = ForeignKey(CompetencyIndicator, verbose_name="Индикатор компетенции", db_index=True, on_delete=CASCADE)
    skill = TextField(verbose_name="Планируемые результаты")
    judging = TextField(verbose_name="Оценочные средства") #перечислениеfos


class RPDDisciplineContent(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    theme = CharField(verbose_name="Тема",max_length=500, db_index=True, default=1)
    content = TextField(verbose_name="Содержимое")


class RPDDisciplineContentHours(Model):
    content = ForeignKey(RPDDisciplineContent, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    hours_type = IntegerField('Тип работы', choices=HourType, db_index=True, default=1)
    hours = IntegerField(verbose_name="Кол-во часов",  db_index=True, default=200)


class ClassType(Model): #подкласс
    name = CharField(verbose_name="Название",max_length=250, db_index=True)


class PracticeDescription(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    theme = ForeignKey(RPDDisciplineContent, verbose_name='Тема', db_index=True, on_delete=CASCADE)
    practice_type = IntegerField('Тип практикума', choices=PracticeType, db_index=True, default=1)
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
    criteria = TextField(verbose_name="Критерии")
    mark = IntegerField(verbose_name="Оценка", choices=ExamMarks.MARKS, db_index=True, default=1)


class FOS(Model): #Общие показатели оценивания?
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    skill = ForeignKey(DisciplineResult, verbose_name='Показатель оценивания', db_index=True, on_delete=CASCADE)
    theme = CharField(verbose_name="Тема", max_length=200, db_index=True, default=1)
    sample = TextField(verbose_name="Образец")


class ELibrary(Model): #подкласс
    name = CharField(verbose_name="Название",max_length=100, db_index=True, default=1)


class Bibliography(Model):
    rpd = ForeignKey(RPDDiscipline, verbose_name="Дисциплина", db_index=True, on_delete=CASCADE)
    reference = TextField(verbose_name="Библиографическая ссылка")
    elibrary = ForeignKey(ELibrary, verbose_name='Электронная литература', null=True, blank=True, db_index=True, on_delete=SET_NULL)
    grif = CharField(verbose_name="Наличие грифа",max_length=200, db_index=True, default=1)
    is_main = BooleanField("Главная литература", default=False)
    count = IntegerField(verbose_name="Кол-во экземпляров", default= 1)

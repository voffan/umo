from datetime import *

from django.db import models, transaction
from django.contrib.auth.models import User


class Person(models.Model):
    FIO = models.CharField(verbose_name="ФИО", max_length=255, db_index=True)
    user = models.ForeignKey(User, verbose_name="Пользователь", db_index=True, blank=True, null=True, on_delete=models.SET_NULL)  # при удалении пользователя, физическое лицо перестанет на него ссылаться

    class Meta:
        verbose_name = 'физическое лицо'
        verbose_name_plural = 'физические лица'

    def __str__(self):
        return self.FIO


class Teacher(Person):

    NONE = 0
    ASSOCIATE = 1
    PROFESSOR = 2

    SCIENTIFIC_TITLE = (
        (NONE, 'без ученого звания'),
        (ASSOCIATE, 'доцент'),
        (PROFESSOR, 'профессор'),
    )

    Position = models.ForeignKey('Position', verbose_name="Должность", db_index=True, null=True, on_delete=models.SET_NULL)  # при удалении должности, преподаватели ее лишаются
    Zvanie = models.IntegerField('ученое звание', choices=SCIENTIFIC_TITLE, blank=True, default=0)
    cathedra = models.ForeignKey('Kafedra', verbose_name="Кафедра", db_index=True, null=True, on_delete=models.SET_NULL)  # при удалении кафедры, преподаватели не будут на него ссылаться

    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'

    def __str__(self):
        return self.FIO


class EduOrg(models.Model):
    name = models.CharField(verbose_name="название института", max_length=200, db_index=True)
    uni = models.ForeignKey('self', verbose_name="Название университета", db_index=True, null=True, blank=True, on_delete=models.SET_NULL)  # при удалении родительского подразделения, дочерние подразделения перестанут ему подчиняться

    class Meta:
        verbose_name = 'подразделение университета'
        verbose_name_plural = 'подразделения университета'

    def __str__(self):
        return self.name


class Kafedra(models.Model):
    number = models.IntegerField(verbose_name="номер кафедры", db_index=True, unique=True)
    name = models.CharField(verbose_name="название кафедры", max_length=200, db_index=True)
    institution = models.ForeignKey('EduOrg', verbose_name="Институт", db_index=True, on_delete=models.CASCADE)  # при удалении института, все его кафедры будут удалены

    class Meta:
        verbose_name = 'кафедра'
        verbose_name_plural = 'кафедры'

    def __str__(self):
        return str(self.number) + '-' + self.name


class EduProg(models.Model):
    specialization = models.ForeignKey('Specialization', verbose_name="Специализация", db_index=True, on_delete=models.CASCADE)  # при удалении специализации будут удалены образовательные программы
    profile = models.ForeignKey('Profile', verbose_name="Профиль", db_index=True, on_delete=models.CASCADE)  # при удалении профиля будут удалены образовательные программы
    year = models.ForeignKey('Year', verbose_name="Год", db_index=True, null=True, on_delete=models.SET_NULL)  # при удалении года в образовательных программах будут очищены ссылки на него
    cathedra = models.ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, on_delete=models.CASCADE)  # при удалении кафедры будут удалены образовательные программы

    class Meta:
        verbose_name = 'образовательная программа'
        verbose_name_plural = 'образовательные программы'

    def __str__(self):
        return self.specialization.name


class Group(models.Model):
    Name = models.CharField(verbose_name="название группы", max_length=200, db_index=True)
    beginyear = models.ForeignKey('Year', verbose_name="Год начала обучения", db_index=True, blank=True, null=True, on_delete=models.SET_NULL)  # при удалении года, в студенческих группах будут очищены ссылки на него
    cathedra = models.ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, blank=True, null=True, on_delete=models.SET_NULL)  # при удалении кафедры, в студенческих группах будет очищены ссылки на нее
    program = models.ForeignKey(EduProg, verbose_name="Программа", db_index=True, blank=True, null=True, on_delete=models.SET_NULL)  # при удалении образовательной программы, в студенческих группах будут очищены ссылки на нее

    class Meta:
        verbose_name = 'студенческая группа'
        verbose_name_plural = 'студенческие группы'
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

    UNDEFINED = 0

    SPECIALIST = 1
    BACHELOR = 2
    MASTER = 3
    BACHELOR_ACADEMIC = 4
    BACHELOR_APPLIED = 5

    QUALIFICATION = (
        (UNDEFINED, '—'),
        (SPECIALIST, 'специалитет'),
        (BACHELOR, 'бакалавриат'),
        (MASTER, 'магистратура'),
        (BACHELOR_ACADEMIC, 'академический бакалавриат'),
        (BACHELOR_APPLIED, 'прикладной бакалавриат'),
    )

    MIDDLE_PROFESSIONAL = 1
    HIGHER_PROFESSIONAL = 2

    EDUCATION_LEVEL = (
        (UNDEFINED, '—'),
        (MIDDLE_PROFESSIONAL, 'среднее профессиональное образование'),
        (HIGHER_PROFESSIONAL, 'высшее профессиональное образование'),
    )

    name = models.CharField(verbose_name="название специализации", max_length=200, db_index=True)
    briefname = models.CharField(verbose_name="короткое имя специализации", max_length=50, db_index=True, blank=True, null=True)
    code = models.CharField(verbose_name="код специализации", max_length=100, db_index=True, unique=True)
    qual = models.IntegerField("квалификация", choices=QUALIFICATION, blank=True, default=0)
    level = models.IntegerField("уровень образования", choices=EDUCATION_LEVEL, blank=True, default=0)

    class Meta:
        verbose_name = 'специализация'
        verbose_name_plural = 'специализации'

    def __str__(self):
        return self.name


class Discipline(models.Model):
    Name = models.CharField(verbose_name="название дисциплины", max_length=200, db_index=True)
    code = models.CharField(verbose_name="код дисциплины", max_length=200, db_index=True)
    program = models.ForeignKey(EduProg, verbose_name="Программа образования", db_index=True, on_delete=models.CASCADE)  # при удалении образовательной программы будут удалены все ее дисциплины

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
            return self.Name


class DisciplineDetails(models.Model):
    discipline = models.ForeignKey(Discipline, verbose_name="Дисциплина", db_index=True, on_delete=models.CASCADE)  # при удалении дисциплины будут удалены все ее варианты
    Credit = models.IntegerField(verbose_name="ЗЕТ", db_index=True, blank=True, null=True)
    Lecture = models.IntegerField(verbose_name="количество лекции", db_index=True, blank=True, null=True)
    Practice = models.IntegerField(verbose_name="количество практики", db_index=True, blank=True, null=True)
    Lab = models.IntegerField(verbose_name="количество лабораторных работ", db_index=True, blank=True, null=True)
    KSR = models.IntegerField(verbose_name="количество контрольно-самостоятельных работ", db_index=True, blank=True, null=True)
    SRS = models.IntegerField(verbose_name="количество срс", db_index=True, blank=True, null=True)
    semestr = models.ForeignKey('Semestr', verbose_name="Семестр", db_index=True, on_delete=models.CASCADE)  # при удалении семестра все варианты дисциплин в этом семестре будут удалены

    class Meta:
        verbose_name = 'вариант дисциплины'
        verbose_name_plural = 'вариант дисциплины'
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

    NONE = 0
    EXAM = 1
    CREDIT = 2
    CREDIT_WITH_GRADE = 3
    COURSEWORK = 4

    CONTROL_FORM = (
        (NONE, 'без контроля'),
        (EXAM, 'экзамен'),
        (CREDIT, 'зачет'),
        (CREDIT_WITH_GRADE, 'зачет с оценкой'),
        (COURSEWORK, 'курсовая работа'),
    )

    discipline_detail = models.ForeignKey('DisciplineDetails',verbose_name="Дисциплина", db_index=True, blank=True, null=True, on_delete=models.CASCADE)  # при удалении варианта дисциплины будут удалены её зачеты и экзамены
    controltype = models.IntegerField('форма контроля', choices=CONTROL_FORM, blank=True, default=0)
    control_hours = models.IntegerField(verbose_name="Кол-во часов", default=0, db_index=True)

    class Meta:
        verbose_name = 'форма промежуточного контроля'
        verbose_name_plural = 'формы промежуточного контроля'
        unique_together=(('discipline_detail','controltype'),)

    def __str__(self):
            return self.get_controltype_display() + ' - ' + self.discipline_detail.discipline.Name + ' - ' \
                   + self.discipline_detail.semestr.name + ' семестр'


class Year(models.Model):
    year = models.IntegerField(verbose_name="год поступления", db_index=True, unique=True)

    class Meta:
        verbose_name = 'год'
        verbose_name_plural = 'год'

    def __str__(self):
            return str(self.year)


class Position(models.Model):
    name = models.CharField(verbose_name="Позиция", db_index=True, max_length=255, unique=True)

    class Meta:
        verbose_name = 'должность'
        verbose_name_plural = 'должности'

    def __str__(self):
        return self.name


class Profile(models.Model):
    spec = models.ForeignKey('Specialization', verbose_name="Специализация", db_index=True, on_delete=models.CASCADE)  # при удалении специализации будут удалены профили
    name = models.CharField(verbose_name="Профиль", db_index=True, max_length=255, unique=True)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'

    def __str__(self):
            return self.spec.name + self.name


class Semestr(models.Model):
    name = models.CharField(verbose_name="Семестр", db_index=True, max_length=255, unique=True)

    class Meta:
        verbose_name = 'семестр'
        verbose_name_plural = 'семестры'

    def __str__(self):
            return self.name


class Mark(models.Model):
    name = models.CharField(verbose_name="Оценка", db_index=True, max_length=255, unique=True)

    class Meta:
        verbose_name = 'оценка'
        verbose_name_plural = 'оценки'

    def __str__(self):
            return self.name


class MarkSymbol(models.Model):
    name = models.CharField(verbose_name="Буквенный эквивалент оценки", db_index=True, blank=True, null=True,
                            max_length=255, unique=True)

    class Meta:
        verbose_name = 'буквенный эквивалент оценки'
        verbose_name_plural = 'буквенные эквиваленты оценок'

    def __str__(self):
            return self.name


class CheckPoint(models.Model):
    name = models.CharField(verbose_name="Срез", db_index=True, max_length=255, unique=True)

    class Meta:
        verbose_name = 'контрольный срез'
        verbose_name_plural = 'контрольные срезы'

    def __str__(self):
            return self.name


class EduPeriod(models.Model):
    beginyear = models.ForeignKey(Year, verbose_name="Начало учебного года", related_name='eduperiod_beginyear', null=True, on_delete=models.SET_NULL)  # при удалении года в образовательных программах будут очищены ссылки
    endyear = models.ForeignKey(Year, verbose_name="Конец учебного года", related_name='eduperiod_endyear', null=True, on_delete=models.SET_NULL)  # при удалении года в образовательных программах будут очищены ссылки
    active = models.BooleanField(verbose_name="Статус", db_index=True)

    class Meta:
        verbose_name = 'период обучения'
        verbose_name_plural = 'периоды обучения'

    def __str__(self):
            return str(self.beginyear.year) + '-' + str(self.endyear.year)


class Student(Person):
    StudentID = models.CharField(verbose_name="Номер зачетной книжки", db_index=True,
                                 max_length=255)

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'

    def __str__(self):
        return self.FIO


class GroupList(models.Model):
    active = models.BooleanField(verbose_name="Статус", db_index=True)
    group = models.ForeignKey('Group', verbose_name="Группа", db_index=True, on_delete=models.CASCADE)  # при удалении группы будут удалены зачисления студентов в нее
    student = models.ForeignKey('Student', verbose_name="Студент", db_index=True, on_delete=models.CASCADE)  # при удалении студента будут удалены его зачисления в группу

    class Meta:
        verbose_name = 'зачисление студента в группу'
        verbose_name_plural = 'зачисления студентов в группы'

    def __str__(self):
            return self.student.FIO + ' - ' + self.group.Name


class Course(models.Model):
    group = models.ForeignKey(Group, verbose_name="Группа", db_index=True, on_delete=models.CASCADE)  # при удалении группы будут удалены её курсы обучения
    discipline_detail = models.ForeignKey(DisciplineDetails, verbose_name="Дисциплина", db_index=True, on_delete=models.CASCADE)  # при удалении варианта дисциплины будут удалены курсы обучения
    lecturer = models.ForeignKey(Teacher, verbose_name="Преподаватель", db_index=True, blank=True, null=True, on_delete=models.SET_NULL)  # при удалении преподавателя в курсах обучения будут очищены ссылки на него

    class Meta:
        verbose_name = 'курс обучения дисциплине'
        verbose_name_plural = 'курсы обучения дисциплинам'

    def __str__(self):
        return self.group.Name + ':' + self.discipline_detail.discipline.Name


class CourseMaxPoints(models.Model):
    course = models.ForeignKey(Course, verbose_name="Курс", db_index=True, on_delete=models.CASCADE)  # при удалении курса обучения будут удалены его максимальные баллы за контрольный срез
    checkpoint = models.ForeignKey(CheckPoint, verbose_name="Срез", db_index=True, on_delete=models.CASCADE)  # при удалении контрольного среза будут удалены максимальные за него
    maxpoint = models.DecimalField(verbose_name="Максимальные баллы", max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'максимальный балл за контрольный срез по дисципине'
        verbose_name_plural = 'максимальные баллы за контрольный срез по дисциплинам'

    def __str__(self):
        return self.course.discipline_detail.discipline.Name + '-' + self.checkpoint.name + ': ' + str(self.maxpoint)


class BRSpoints(models.Model):
    student = models.ForeignKey(Student, db_index=True, on_delete=models.CASCADE)  # при удалении студента будут удалены его баллы
    checkpoint = models.ForeignKey(CheckPoint, db_index=True, on_delete=models.CASCADE)  # при удалении контрольного среза среза будут удалены его баллы
    points = models.FloatField(verbose_name="Баллы", db_index=True, max_length=255)
    course = models.ForeignKey(Course, db_index=True, on_delete=models.CASCADE)  # при удалении дисциплины будут удалены ее баллы

    class Meta:
        verbose_name = 'балл БРС'
        verbose_name_plural = 'баллы БРС'
        permissions = (
            ('can_view_scores', 'Can view students brs scores'),
        )

    def __str__(self):
        return self.student.FIO + ' - ' + self.course.discipline_detail.discipline.Name


class Exam(models.Model):
    examDate = models.CharField(verbose_name="Дата экзамена", db_index=True, max_length=255)
    course = models.ForeignKey(Course, db_index=True, on_delete=models.CASCADE)  # при удалении дисциплины будут удалены его зачеты и экзамены
    controlType = models.IntegerField('форма контроля', choices=Control.CONTROL_FORM)
    prev_exam = models.ForeignKey('self', verbose_name="Предыдущий экзамен", blank=True, null=True, on_delete=models.SET_NULL)  # при удалении предыдущего экзамена ссылка на него очищается

    class Meta:
        verbose_name = 'контрольное мероприятие для курса обучения дисциплине'
        verbose_name_plural = 'контрольные мероприятия для курсов обучения дисциплнам'

    def __str__(self):
        return self.course.discipline_detail.discipline.Name + '"' + self.examDate + '"'


class ExamMarks(models.Model):
    exam = models.ForeignKey(Exam, db_index=True, on_delete=models.CASCADE)  # при удалении экзамена будут удалены все его сдачи
    student = models.ForeignKey(Student, db_index=True, on_delete=models.CASCADE)  # при удалении студента будут удалены все его сдачи экзаменов
    inPoints = models.FloatField(verbose_name="Баллы за срез", max_length=255)
    additional_points = models.FloatField(verbose_name="Баллы за отработку", blank=True, null=True, max_length=255)
    examPoints = models.FloatField(verbose_name="Баллы за экзамен", blank=True, null=True, max_length=255)
    mark = models.ForeignKey(Mark, db_index=True, on_delete=models.CASCADE)  # при удалении оценки будут удалены все сдачи экзаменов на эту оценку
    markSymbol = models.ForeignKey(MarkSymbol, db_index=True, blank=True, null=True, on_delete=models.SET_NULL)  # при удалении буквенного обозначения ссылка на него в сдачах будет очищена

    class Meta:
        verbose_name = 'экзаменационная оценка'
        verbose_name_plural = 'экзаменационные оценки'

    def __str__(self):
        return self.student.FIO + ' - ' + self.exam.course.discipline_detail.discipline.Name + ' - ' + self.mark.name


class Synch(models.Model):
    date = models.DateTimeField()
    finished = models.BooleanField()

    class Meta:
        verbose_name = 'признак успешного завершения редактирования зачисления студентов в группу'
        verbose_name_plural = 'признаки успешного завершения редактирования зачисления студентов в группу'

    def __str__(self):
        return 'None'

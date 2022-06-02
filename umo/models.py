from datetime import datetime

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models import CharField, TextField, ForeignKey, IntegerField, BooleanField, DecimalField, FloatField, DateTimeField
from django.db.models import Model, CASCADE, SET_NULL


class Person(Model):
    FIO = CharField(verbose_name="ФИО", max_length=255, db_index=True)
    last_name = CharField(verbose_name="фамилия", max_length=50, default='')
    first_name = CharField(verbose_name="имя", max_length=50, default='')
    second_name = CharField(verbose_name="отчество", max_length=50, default='')
    maiden_name = CharField(verbose_name="девичья фамилия", max_length=50, default='', blank=True)
    user = ForeignKey(User, verbose_name="пользователь", db_index=True, blank=True, null=True, on_delete=SET_NULL)

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

    position = ForeignKey('Position', verbose_name="должность", db_index=True, null=True, on_delete=SET_NULL)
    title = IntegerField('ученое звание', choices=SCIENTIFIC_TITLE, blank=True, default=0)
    cathedra = ForeignKey('Kafedra', verbose_name="кафедра", db_index=True, null=True, on_delete=SET_NULL)

    class Meta:
        verbose_name = 'преподаватель'
        verbose_name_plural = 'преподаватели'


class EduOrg(Model):
    name = CharField(verbose_name="название института", max_length=200, db_index=True)
    uni = ForeignKey('self', verbose_name="название университета", db_index=True, null=True, blank=True,
                     on_delete=SET_NULL)

    class Meta:
        verbose_name = 'подразделение университета'
        verbose_name_plural = 'подразделения университета'

    def __str__(self):
        return self.name


class Kafedra(Model):
    number = IntegerField(verbose_name="номер кафедры", db_index=True, unique=True)
    name = CharField(verbose_name="название кафедры", max_length=200, db_index=True)
    institution = ForeignKey('EduOrg', verbose_name="институт", db_index=True, on_delete=CASCADE)

    class Meta:
        verbose_name = 'кафедра'
        verbose_name_plural = 'кафедры'

    def __str__(self):
        return str(self.number) + '-' + self.name


class EduProgram(Model):
    name = CharField(verbose_name="Имя плана подготовки", db_index=True, max_length=100)
    specialization = ForeignKey('Specialization', verbose_name="специализация", db_index=True, on_delete=CASCADE)
    profile = ForeignKey('Profile', verbose_name="профиль", db_index=True, on_delete=CASCADE)
    year = ForeignKey('Year', verbose_name="год", db_index=True, null=True, on_delete=SET_NULL)
    cathedra = ForeignKey(Kafedra, verbose_name="кафедра", db_index=True, on_delete=CASCADE)

    class Meta:
        verbose_name = 'образовательная программа'
        verbose_name_plural = 'образовательные программы'

    def __str__(self):
        return '%s (%d)' % (self.specialization.name, self.year.year)


class Group(Model):
    Name = CharField(verbose_name="название группы", max_length=200, db_index=True)
    begin_year = ForeignKey('Year', verbose_name="год начала обучения", db_index=True, blank=True, null=True,
                            on_delete=SET_NULL)
    cathedra = ForeignKey('Kafedra', verbose_name="кафедра", db_index=True, blank=True, null=True, on_delete=SET_NULL)
    program = ForeignKey('EduProgram', verbose_name="программа", db_index=True, blank=True, null=True,
                         on_delete=SET_NULL)

    class Meta:
        verbose_name = 'студенческая группа'
        verbose_name_plural = 'студенческие группы'
        ordering = ['Name']

    def __str__(self):
        return self.Name

    @property
    def year(self):
        now = datetime.now()
        t = int(now.year) - self.begin_year.year
        return t + int(now.month >= 8)

    @property
    def current_semester(self):
        edu_period = EduPeriod.objects.get(active=True)
        addition = 1
        current_month = datetime.today().month
        if current_month >= 2 and current_month <= 8:
            addition = 2
        return str((edu_period.begin_year.year - self.begin_year.year) * 2 + addition)


    def get_semesters(self, edu_period):
        try:
            autumn_semester = Semester.objects.get(name=str((edu_period.begin_year.year - self.begin_year.year) * 2 + 1))
            spring_semester = Semester.objects.get(name=str((edu_period.begin_year.year - self.begin_year.year) * 2 + 2))
        except Exception:
            raise Exception('Система не настроена!! Нет соответствущих учебному году семестров!!')
        return autumn_semester.id, spring_semester.id

    def add_discipline(self, discipline):
        course = Course()
        course.group = self
        course.discipline_detail = discipline
        course.lecturer = None
        course.save()

    def fill_group_disciplines(self, edu_period=None, semester=None):
        if self.program is None:
            raise Exception('Для группы не определена программа обучения!! Исправьте!!')
        if edu_period is None:
            try:
                edu_period = EduPeriod.objects.get(active=True)
            except Exception:
                raise Exception('Система не настроена! Вы не определили активный учебный год или их несколько!!!')
        if semester is None:
            semesters = self.get_semesters(edu_period)
        else:
            semesters = [Semester.objects.filter(name=semester).first().id]
        ids = list(
            Course.objects.filter(group__id=self.id, discipline_detail__semester__id__in=semesters).
                values_list('discipline_detail__id', flat=True))
        disciplines_details = DisciplineDetails.objects.filter(discipline__program__id=self.program.id,
                                                               semester__id__in=semesters).exclude(id__in=ids)
        with transaction.atomic():
            for discipline_detail in disciplines_details:
                self.add_discipline(discipline_detail)


class Specialization(Model):

    UNDEFINED = 0

    SPECIALIST = 1
    BACHELOR = 2
    MASTER = 3
    BACHELOR_ACADEMIC = 4
    BACHELOR_APPLIED = 5
    MASTER_ACADEMIC = 6
    MASTER_APPLIED = 7
    POSTGRADUATE = 8
    INTERN = 9


    QUALIFICATION = (
        (UNDEFINED, '—'),
        (SPECIALIST, 'специалитет'),
        (BACHELOR, 'бакалавриат'),
        (MASTER, 'магистратура'),
        (BACHELOR_ACADEMIC, 'академический бакалавриат'),
        (BACHELOR_APPLIED, 'прикладной бакалавриат'),
        (MASTER_ACADEMIC, 'академическая магистратура'),
        (MASTER_APPLIED, 'прикладная магистратура'),
        (POSTGRADUATE, 'аспирантура'),
        (INTERN, 'ординатура'),
    )

    MIDDLE_PROFESSIONAL = 1
    HIGHER_PROFESSIONAL = 2

    EDUCATION_LEVEL = (
        (UNDEFINED, '—'),
        (MIDDLE_PROFESSIONAL, 'среднее профессиональное образование'),
        (HIGHER_PROFESSIONAL, 'высшее профессиональное образование'),
    )

    name = CharField(verbose_name="название специализации", max_length=200, db_index=True)
    brief_name = CharField(verbose_name="короткое имя специализации", max_length=50, db_index=True, blank=True,
                           null=True)
    code = CharField(verbose_name="код специализации", max_length=100, db_index=True)
    qual = IntegerField("квалификация", choices=QUALIFICATION, blank=True, default=0)
    level = IntegerField("уровень образования", choices=EDUCATION_LEVEL, blank=True, default=0)

    class Meta:
        verbose_name = 'специализация'
        verbose_name_plural = 'специализации'
        unique_together = ('code', 'qual')

    def __str__(self):
        return self.name


class Discipline(Model):
    Name = CharField(verbose_name="название дисциплины", max_length=200, db_index=True)
    code = CharField(verbose_name="код дисциплины", max_length=200, db_index=True)
    program = ForeignKey('EduProgram', verbose_name="программа образования", db_index=True, on_delete=CASCADE)

    class Meta:
        verbose_name = 'дисциплина'
        verbose_name_plural = 'дисциплины'

    def __str__(self):
            return self.Name


class DisciplineDetails(Model):
    discipline = ForeignKey(Discipline, verbose_name="дисциплина", db_index=True, on_delete=CASCADE)
    Credit = IntegerField(verbose_name="ЗЕТ", db_index=True, blank=True, null=True)
    Lecture = IntegerField(verbose_name="количество лекции", db_index=True, blank=True, null=True)
    Practice = IntegerField(verbose_name="количество практики", db_index=True, blank=True, null=True)
    Lab = IntegerField(verbose_name="количество лабораторных работ", db_index=True, blank=True, null=True)
    KSR = IntegerField(verbose_name="количество контрольно-самостоятельных работ", db_index=True, blank=True, null=True)
    SRS = IntegerField(verbose_name="количество срс", db_index=True, blank=True, null=True)
    semester = ForeignKey('Semester', verbose_name="семестр", db_index=True, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'вариант дисциплины'
        verbose_name_plural = 'вариант дисциплины'
        unique_together = (('discipline', 'semester'),)

    def __str__(self):
            return self.discipline.Name + ' - ' + self.semester.name + ' семестр'

    @property
    def total_hours(self):
        exam_hours = 0
        for control in self.control_set:
            if control.control_type == Control.EXAM:
                exam_hours = 36
                break
        return self.Lecture + self.Practice + self.Lab + self.KSR + self.SRS + exam_hours

    @property
    def controls(self):
        return ', '.join(map(lambda x: Control.CONTROL_FORM[x][1], list(self.control_set.all().values_list('control_type', flat=True))))

    @property
    def controls_list(self):
        return [(control.id, Control.CONTROL_FORM[control.control_type][1]) for control in self.control_set.all()]


class Control(Model):

    NONE = 0
    EXAM = 1
    CREDIT = 2
    CREDIT_WITH_GRADE = 3
    COURSEWORK = 4
    COURSEPROJECT = 5
    TEST = 6
    HOMETEST = 7
    GRADE = 8
    ESSAY = 9
    REVIEW = 10
    RGR = 11
    OTHERS = 49

    CONTROL_FORM = (
        (NONE, 'без контроля'),
        (EXAM, 'экзамен'),
        (CREDIT, 'зачет'),
        (CREDIT_WITH_GRADE, 'зачет с оценкой'),
        (COURSEWORK, 'курсовая работа'),
        (COURSEPROJECT, "Курсовой проект"),
        (TEST, "Контрольная работа"),
        (HOMETEST, "Домашняя контрольная работа"),
        (GRADE, "Оценка"),
        (ESSAY, "Эссе"),
        (REVIEW, "Реферат"),
        (RGR, "Расчетно-графическая работа"),
        (OTHERS, "Другие формы контроля"),
    )

    discipline_detail = ForeignKey('DisciplineDetails', verbose_name="дисциплина", db_index=True, blank=True, null=True,
                                   on_delete=CASCADE)
    control_type = IntegerField('форма контроля', choices=CONTROL_FORM, blank=True, default=0)
    control_hours = IntegerField(verbose_name="кол-во часов", default=0, db_index=True)

    class Meta:
        verbose_name = 'форма промежуточного контроля'
        verbose_name_plural = 'формы промежуточного контроля'
        unique_together = (('discipline_detail', 'control_type'),)

    def __str__(self):
        return self.get_control_type_display() + ' - ' + self.discipline_detail.discipline.Name + ' - ' \
               + self.discipline_detail.semester.name + ' семестр'


class Year(Model):
    year = IntegerField(verbose_name="год поступления", db_index=True, unique=True)

    class Meta:
        verbose_name = 'год'
        verbose_name_plural = 'год'

    def __str__(self):
            return str(self.year)


class Position(Model):
    name = CharField(verbose_name="позиция", db_index=True, max_length=255, unique=True)

    class Meta:
        verbose_name = 'должность'
        verbose_name_plural = 'должности'

    def __str__(self):
        return self.name


class Profile(Model):
    spec = ForeignKey('Specialization', verbose_name="специализация", db_index=True, on_delete=CASCADE)
    name = CharField(verbose_name="профиль", db_index=True, max_length=255)

    class Meta:
        verbose_name = 'профиль'
        verbose_name_plural = 'профили'
        unique_together = ['spec', 'name']

    def __str__(self):
            return self.spec.name + self.name


class Semester(Model):
    name = CharField(verbose_name="семестр", db_index=True, max_length=255, unique=True)

    class Meta:
        verbose_name = 'семестр'
        verbose_name_plural = 'семестры'

    def __str__(self):
            return self.name


class CheckPoint(Model):
    name = CharField(verbose_name="срез", db_index=True, max_length=255, unique=True)

    class Meta:
        verbose_name = 'контрольный срез'
        verbose_name_plural = 'контрольные срезы'

    def __str__(self):
        return self.name


class EduPeriod(Model):
    begin_year = ForeignKey(Year, verbose_name="начало учебного года", related_name='edu_period_begin_year', null=True,
                            on_delete=SET_NULL)
    end_year = ForeignKey(Year, verbose_name="конец учебного года", related_name='edu_period_end_year', null=True,
                          on_delete=SET_NULL)
    active = BooleanField(verbose_name="статус", db_index=True)

    class Meta:
        verbose_name = 'период обучения'
        verbose_name_plural = 'периоды обучения'

    def __str__(self):
            return str(self.begin_year.year) + '-' + str(self.end_year.year)


class Student(Person):
    student_id = CharField(verbose_name="номер зачетной книжки", db_index=True, max_length=255)

    class Meta:
        verbose_name = 'студент'
        verbose_name_plural = 'студенты'


class GroupList(Model):
    active = BooleanField(verbose_name="статус", db_index=True)
    group = ForeignKey('Group', verbose_name="группа", db_index=True, on_delete=CASCADE)
    student = ForeignKey('Student', verbose_name="студент", db_index=True, on_delete=CASCADE)

    class Meta:
        verbose_name = 'зачисление студента в группу'
        verbose_name_plural = 'зачисления студентов в группы'

    def __str__(self):
            return self.student.FIO + ' - ' + self.group.Name


class Course(Model):
    group = ForeignKey(Group, verbose_name="группа", db_index=True, on_delete=CASCADE)
    discipline_detail = ForeignKey(DisciplineDetails, verbose_name="дисциплина", db_index=True, on_delete=CASCADE)
    lecturer = ForeignKey(Teacher, verbose_name="преподаватель", db_index=True, blank=True, null=True,
                          on_delete=SET_NULL)
    is_finished = BooleanField('Курс окончен', default=False)

    class Meta:
        verbose_name = 'курс обучения дисциплине'
        verbose_name_plural = 'курсы обучения дисциплинам'

    def __str__(self):
        return self.group.Name + ':Семестр ' + self.discipline_detail.semester.name + ':' + self.discipline_detail.discipline.Name


class CourseMaxPoints(Model):
    course = ForeignKey(Course, verbose_name="курс", db_index=True, on_delete=CASCADE)
    checkpoint = ForeignKey(CheckPoint, verbose_name="срез", db_index=True, on_delete=CASCADE)
    max_point = DecimalField(verbose_name="максимальные баллы", default=100, max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'максимальный балл за контрольный срез по дисципине'
        verbose_name_plural = 'максимальные баллы за контрольный срез по дисциплинам'

    def __str__(self):
        return self.course.discipline_detail.discipline.Name + '-' + self.checkpoint.name + ': ' + str(self.max_point)


class BRSpoints(Model):
    student = ForeignKey(Student, db_index=True, on_delete=CASCADE)
    checkpoint = ForeignKey(CheckPoint, db_index=True, on_delete=CASCADE)
    points = FloatField(verbose_name="баллы", db_index=True, max_length=255)
    course = ForeignKey(Course, db_index=True, on_delete=CASCADE)

    class Meta:
        verbose_name = 'балл БРС'
        verbose_name_plural = 'баллы БРС'
        permissions = (
            ('can_view_scores', 'Can view students brs scores'),
        )

    def __str__(self):
        return self.student.FIO + ' - ' + self.course.discipline_detail.discipline.Name


class Exam(Model):
    examDate = DateTimeField(verbose_name="дата экзамена", db_index=True, auto_now_add=True)
    course = ForeignKey(Course, db_index=True, on_delete=CASCADE)
    controlType = IntegerField('форма контроля', choices=Control.CONTROL_FORM)
    prev_exam = ForeignKey('self', verbose_name="предыдущий экзамен", blank=True, null=True, on_delete=SET_NULL)
    is_finished = BooleanField('Экзамен закончен', default=False)

    class Meta:
        verbose_name = 'контрольное мероприятие для курса обучения дисциплине'
        verbose_name_plural = 'контрольные мероприятия для курсов обучения дисциплинам'

    def __str__(self):
        return self.course.discipline_detail.discipline.Name + '"' + self.examDate.strftime('%d.%m.%Y') + '"'


class ExamMarks(Model):
    SYMBOL_MARK = (
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
        ('FX', 'FX'),
        ('F', 'F'),
    )

    MARKS = (
        (0, "Неявка"),
        (1, "Индивидуальный план"),
        (2, "Неудовлетворительно"),
        (3, "Удовлетворительно"),
        (4, "Хорошо"),
        (5, "Отлично"),
        (6, "Зачтено"),
        (7, "Не зачтено"),
        (8, "Не допущен"),
        (9, "---")
    )

    exam = ForeignKey(Exam, db_index=True, on_delete=CASCADE)
    student = ForeignKey(Student, db_index=True, on_delete=CASCADE)
    inPoints = FloatField(verbose_name="баллы за срез", max_length=255)
    additional_points = FloatField(verbose_name="баллы за отработку", blank=True, null=True, max_length=255)
    examPoints = FloatField(verbose_name="баллы за экзамен", blank=True, null=True, max_length=255)
    mark = IntegerField(verbose_name='Оценка', choices=MARKS, db_index=True, default=0)
    mark_symbol = CharField('буквенный эквивалент оценки', max_length=2, default='')

    class Meta:
        verbose_name = 'экзаменационная оценка'
        verbose_name_plural = 'экзаменационные оценки'

    def __str__(self):
        return self.student.FIO + ' - ' + self.exam.course.discipline_detail.discipline.Name + ' - ' + self.MARKS[self.mark][1]

    @property
    def total_points(self):
        return self.inPoints + self.additional_points + self.examPoints

    def get_mark_symbol(self):
        points = self.total_points
        symbol = ExamMarks.SYMBOL_MARK[6][0]
        if points >= 25 and points < 55:
            symbol = ExamMarks.SYMBOL_MARK[5][0]
        elif points >= 55 and points < 65:
            symbol = ExamMarks.SYMBOL_MARK[4][0]
        elif points >= 65 and points < 75:
            symbol = ExamMarks.SYMBOL_MARK[3][0]
        elif points >= 75 and points < 85:
            symbol = ExamMarks.SYMBOL_MARK[2][0]
        elif points >= 85 and points < 95:
            symbol = ExamMarks.SYMBOL_MARK[1][0]
        elif points >= 95 and points <= 100:
            symbol = ExamMarks.SYMBOL_MARK[0][0]
        return symbol

    def get_control_mark(self):
        points = self.total_points
        mark = 9
        if self.exam.controlType != Control.NONE and self.exam.controlType != Control.CREDIT:
            if 0 <= points < 45 and self.exam.controlType == Control.EXAM:
                mark = 8
            elif 0 <= points < 55:
                mark = 2
            elif 55 <= points < 65:
                mark = 3
            elif 65 <= points < 85:
                mark = 4
            elif 85 <= points <= 100:
                mark = 5
        elif self.exam.controlType == Control.CREDIT:
            mark = 6
            if 0 <= points < 60:
                mark = 7
        return mark

    def save(self, *args, **kwargs):
        if self.mark > 1 and self.mark != 8:
            if self.exam.controlType == 2:
                self.examPoints = 0
            self.mark = self.get_control_mark()
            self.mark_symbol = self.get_mark_symbol()
        else:
            self.examPoints = 0
        super().save(*args, **kwargs)

    @property
    def mark_to_text(self):
        return self.MARKS[self.mark][1]


class Synch(Model):
    date = DateTimeField('Дата синхронизации')
    finished = BooleanField('Синхронизация не выполнена')

    class Meta:
        verbose_name = 'признак успешного завершения редактирования зачисления студентов в группу'
        verbose_name_plural = 'признаки успешного завершения редактирования зачисления студентов в группу'

    def __str__(self):
        return 'None'


class Competency(Model):
    UK = 1
    OPK = 2
    PK = 3

    CompetencyType =(
        (UK,"Универсальные"),
        (OPK,"Общепрофессиональные"),
        (PK,"Профессиональные"),
    )

    edu_program = ForeignKey(EduProgram, verbose_name="Программа обучения", db_index=True, on_delete=CASCADE)
    type = IntegerField("Вид компетенции", choices=CompetencyType, db_index=True, default=UK)
    short_name = CharField(verbose_name="Абривиатура", max_length=20, db_index=True, default=1)
    name = CharField(verbose_name="Название", max_length=250, db_index=True, default=1)

    def __str__(self):
        return self.name


class CompetencyIndicator(Model):
    competency = ForeignKey(Competency, verbose_name="Компетенция", db_index=True, on_delete=CASCADE)
    short_name = CharField(verbose_name="Название", max_length=20, db_index=True, default=1)
    indicator = CharField(verbose_name="Индикаторы", max_length=500, default='indicator')

    def __str__(self):
        self.short_name + ": " + str(self.indicator)

from django.db import models

from django.db import models, transaction
from django.db.models import CharField, ForeignKey, IntegerField, BooleanField, DecimalField, FloatField, DateTimeField, OneToOneField
from django.db.models import Model, CASCADE, SET_NULL
from django.core.validators import MaxValueValidator, MinValueValidator
from umo.models import Teacher, Course, Specialization, EduOrg, Group, DisciplineDetails, EduPeriod, Kafedra


class DisciplineSetting(DisciplineDetails):
    is_lecture_seperate = BooleanField(verbose_name="Лекции отдельно", default=False)
    practice_weekly = DecimalField(verbose_name="Недель практики", max_digits=6, decimal_places=2, default=0)
    is_hourly = BooleanField(verbose_name="Почасовая", default=False)
    is_KR_KP_VKR = BooleanField(verbose_name="КР/КП ВКР", default=False)
    is_new = BooleanField(verbose_name="Вновь вводимый", default=False)
    need_new_RPD = BooleanField(verbose_name="Составление РПД", default=False)
    need_upd_RPD = BooleanField(verbose_name="Обновление РПД", default=False)

    class Meta:
        verbose_name = 'Настройки дисциплины'
        verbose_name_plural = 'Настройки дисциплин'


class GroupInfo(Model):
    PLANNED = 1
    COMMERCIAL = 2

    GROUP_TYPE = (
        (PLANNED, 'Плановый'),
        (COMMERCIAL, 'Коммерческий'),
    )

    SUBGROUP = (
        (1, 'Одна'),
        (2, 'Две'),
        (3, 'Три'),
    )

    group = ForeignKey(Group, verbose_name="группа", db_index=True, on_delete=CASCADE)
    group_type = IntegerField('Тип группы', choices=GROUP_TYPE, default=1)
    subgroup = IntegerField("Количество подгрупп", choices=SUBGROUP, default=1)
    amount = IntegerField("Количество студентов", default=1, validators=[MaxValueValidator(30), MinValueValidator(1)])

    class Meta:
        verbose_name = 'Информация о группе'
        verbose_name_plural = 'Информация о группах'

    def __str__(self):
        return self.group.Name


class CourseHours(Model):
    edu_period = ForeignKey(EduPeriod, verbose_name="Учебный год", db_index=True, on_delete=CASCADE)
    teacher = ForeignKey(Teacher, verbose_name="Преподаватель", db_index=True, blank=True, null=True, on_delete=SET_NULL)
    group = ForeignKey(GroupInfo, verbose_name="группа", db_index=True, on_delete=CASCADE)
    cathedra = ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, blank=True, null=True, on_delete=CASCADE)
    discipline_settings = ForeignKey(DisciplineSetting, verbose_name="дисциплина", db_index=True, on_delete=CASCADE)
    f_lecture = IntegerField(verbose_name="Лекции", default=0)
    f_practice = IntegerField(verbose_name="Практики", default=0)
    f_lab = IntegerField(verbose_name="Лабораторные работы", default=0)
    f_consult_hours = IntegerField(verbose_name="Консультации", default=0)
    f_exam_hours = IntegerField(verbose_name="Экзамены", default=0)
    f_control_hours = IntegerField(verbose_name="Проверка РГР", default=0)
    f_check_hours = IntegerField(verbose_name="Проверка остаточных знаний", default=0)
    f_control_SRS = IntegerField(verbose_name="Контроль СРС", default=0)
    f_control_BRS = IntegerField(verbose_name="Контроль БРС", default=0)

    class Meta:
        verbose_name = 'Часы дисциплины'
        verbose_name_plural = 'Часы дисциплин'
        #unique_together = ['teacher', 'group', 'edu_period']

    def __str__(self):
        return self.discipline_settings.discipline.Name


class SupervisionHours(Model):
    VKR = 1
    KPKR = 2
    POSTGRADUATE = 3
    MASTER = 4
    MASTERPROG = 5

    SUPERVISION_TYPE = (
        (VKR, "ВКР"),
        (KPKR, "КП/КР"),
        (POSTGRADUATE, "Аспирантами"),
        (MASTER, "Магистрантами"),
        (MASTERPROG, "Программой магистрантов"),
    )

    teacher = ForeignKey(Teacher, verbose_name="Преподаватель", db_index=True, blank=True, null=True, on_delete=CASCADE)
    group = ForeignKey(GroupInfo, verbose_name="группа", db_index=True, on_delete=CASCADE)
    students = IntegerField(verbose_name="Количество студентов", default=0)
    supervision_type = IntegerField(verbose_name="Руководство", choices=SUPERVISION_TYPE, db_index=True, default=1)
    hours = IntegerField(verbose_name="Часы", default=0)
    edu_period = ForeignKey(EduPeriod, verbose_name="Учебный год", db_index=True, on_delete=CASCADE)
    cathedra = ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, blank=True, null=True, on_delete=CASCADE)
    
    class Meta:
        verbose_name = 'Руководство'
        verbose_name_plural = 'Руководства'
        unique_together = ['teacher', 'group', 'supervision_type', 'edu_period']


class PracticeHours(Model):
    EDU = 1
    INTERN = 2
    GRADUATE = 3
    TEACHING = 4

    PRACTICE_TYPE = (
        (EDU, "ВКР"),
        (INTERN, "КП/КР"),
        (GRADUATE, "Аспирантами"),
        (TEACHING, "Магистрантами"),
    )

    teacher = ForeignKey(Teacher, verbose_name="Преподаватель", db_index=True, blank=True, null=True, on_delete=CASCADE)
    group = ForeignKey(GroupInfo, verbose_name="группа", db_index=True, on_delete=CASCADE)
    practice_type = IntegerField(verbose_name="Руководство практики", choices=PRACTICE_TYPE, db_index=True, default=1)
    hours = IntegerField(verbose_name="Часы", default=0)
    edu_period = ForeignKey(EduPeriod, verbose_name="Учебный год", db_index=True, on_delete=CASCADE)
    cathedra = ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, blank=True, null=True, on_delete=CASCADE)
    
    class Meta:
        verbose_name = 'Руководство практики'
        verbose_name_plural = 'Руководства практик'
        unique_together = ['teacher', 'group', 'practice_type', 'edu_period']


class OtherHours(Model):
    GEK = 1
    VKRREV = 2
    ADMIS = 3
    REFREV = 4

    OTHER_TYPE = (
        (GEK, "ГЭК, ГАК"),
        (VKRREV, "Рецензия ВКР"),
        (ADMIS, "Прием кандидатского"),
        (REFREV, "Рецензия рефератов"),
    )

    teacher = ForeignKey(Teacher, verbose_name="Преподаватель", db_index=True, blank=True, null=True, on_delete=CASCADE)
    group = ForeignKey(GroupInfo, verbose_name="Группа", db_index=True, on_delete=CASCADE)
    other_type = IntegerField(verbose_name="Тип", choices=OTHER_TYPE, db_index=True, default=1)
    hours = IntegerField(verbose_name="Часы", default=0)
    edu_period = ForeignKey(EduPeriod, verbose_name="Учебный год", db_index=True, on_delete=CASCADE)
    cathedra = ForeignKey(Kafedra, verbose_name="Кафедра", db_index=True, blank=True, null=True, on_delete=CASCADE)

    class Meta:
        verbose_name = 'Остальные часы'
        verbose_name_plural = 'Остальные часы'
        unique_together = ['teacher', 'group', 'other_type', 'edu_period']


class CathedraEmployee(Model):
    FULLTIME = 0
    PARTTIME = 1
    HOURLY = 2

    STAFF_TYPE = (
        (FULLTIME, 'Штатный'),
        (PARTTIME, 'Совместитель'),
        (HOURLY, 'Почасовик'),
    )

    teacher = ForeignKey(Teacher, verbose_name="преподаватель", db_index=True, null=True, on_delete=CASCADE)
    stavka = FloatField(verbose_name="ставка преподавателя", default=0)
    employee_type = IntegerField(verbose_name="тип", choices=STAFF_TYPE, blank=True, default=0)
    is_active = BooleanField(verbose_name="преподаватель активен")

    class Meta:
        verbose_name = 'Работник кафедры'
        verbose_name_plural = 'Работники кафедры'
    



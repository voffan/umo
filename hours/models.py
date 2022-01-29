from django.db import models

from django.db import models, transaction
from django.db.models import CharField, ForeignKey, IntegerField, BooleanField, DecimalField, FloatField, DateTimeField
from django.db.models import Model, CASCADE, SET_NULL
from django.core.validators import MaxValueValidator, MinValueValidator
from umo.models import Teacher, Course, Specialization, EduOrg, Group

class ActualCourse(Course):
    f_credit = IntegerField(verbose_name="ЗЕТ", default=0)
    f_lecture = IntegerField(verbose_name="Лекции", default=0)
    f_practice = IntegerField(verbose_name="Практики", default=0)
    f_lab = IntegerField(verbose_name="Лабораторные работы", default=0)
    f_ksr = IntegerField(verbose_name="КСР", default=0)
    f_srs = IntegerField(verbose_name="СРС", default=0)
    is_lecture_seperate = BooleanField(verbose_name="Лекции отдельно", default=False)
    practice_weekly = DecimalField(verbose_name="Недель практики", max_digits=6, decimal_places=2, default=0)
    is_hourly = BooleanField(verbose_name="Почасовая", default=False)
    is_KR_KP_VKR = BooleanField(verbose_name="КР/КП ВКР", default=False)
    is_new = BooleanField(verbose_name="Вновь вводимый", default=False)
    need_new_RPD = BooleanField(verbose_name="Составление РПД", default=False)
    need_upd_RPD = BooleanField(verbose_name="Обновление РПД", default=False)
    #lab_teacher = ForeignKey(Teacher, verbose_name="" on_delete)

    class Meta:
        verbose_name = 'фактические часы курса обучения'
        verbose_name_plural = 'фактические часы курса обучения'

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

class GroupInfo(Model):
    SUBGROUP = (
        (1, 'Одна'),
        (2, 'Две'),
        (3, 'Три'),
    )
    PLANNED = 1
    COMMERCIAL = 2
    GROUP_TYPE = (
        (PLANNED, 'Плановый'),
        (COMMERCIAL, 'Коммерческий'),
    )

    group = ForeignKey(Group, verbose_name="группа", db_index=True, on_delete=CASCADE)
    group_type = IntegerField('Тип группы', choices=GROUP_TYPE, default=1)
    subgroup = IntegerField("Количество подгрупп", choices=SUBGROUP, default=1)
    amount = IntegerField("Количество студентов", default=1, validators=[MaxValueValidator(30), MinValueValidator(1)])
    



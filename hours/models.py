from django.db import models

from django.db import models, transaction
from django.db.models import CharField, ForeignKey, IntegerField, BooleanField, DecimalField, FloatField, DateTimeField
from django.db.models import Model, CASCADE, SET_NULL
from umo.models import Teacher, Course

class ActualCourse(Course):
    f_credit = IntegerField(verbose_name="ЗЕТ", db_index=True, blank=True, null=True)
    f_lecture = IntegerField(verbose_name="Лекции", db_index=True, blank=True, null=True)
    f_practice = IntegerField(verbose_name="Практики", db_index=True, blank=True, null=True)
    f_lab = IntegerField(verbose_name="Лабораторные работы", db_index=True, blank=True, null=True)
    f_ksr = IntegerField(verbose_name="КСР", db_index=True, blank=True, null=True)
    f_srs = IntegerField(verbose_name="СРС", db_index=True, blank=True, null=True)

    class Meta:
        verbose_name = 'фактические часы курса обучения'
        verbose_name_plural = 'фактические часы курса обучения'

class CathedraEmployee(Model):
    FULLTIME = 0
    PARTTIME = 1
    HOURLY = 2

    STAFF_TYPE = (
        (FULLTIME, 'штатные'),
        (PARTTIME, 'совместители'),
        (HOURLY, 'почасовики'),
    )
    teacher = ForeignKey(Teacher, verbose_name="преподаватель", db_index=True, null=True, on_delete=CASCADE)
    stavka = FloatField(verbose_name="ставка преподавателя", db_index=True, blank=True, null=True)
    employee_type = IntegerField('', choices=STAFF_TYPE, blank=True, default=0)
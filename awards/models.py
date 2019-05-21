from umo.models import Teacher, Person
from django.db.models import CharField, ForeignKey, DateTimeField, DateField, IntegerField
from django.db.models import Model, CASCADE, SET_NULL
from djangoyearlessdate.models import YearField


class Award(Model):
    NONE = 0
    FEDERAL = 1
    REGIONAL = 2
    OCCUPATION = 3
    USSR = 4

    AWARD_LEVEL = (
        (NONE, '----'),
        (FEDERAL, 'Федеральный'),
        (REGIONAL, 'Республиканский'),
        (OCCUPATION, 'Отрослевой'),
        (USSR, 'Всесоюзный'),
    )

    award_type = ForeignKey('AwardType', verbose_name='Тип награды', on_delete=CASCADE)
    award_name = CharField(verbose_name='Наименование награды', db_index=True, max_length=250)
    issuer = ForeignKey('Issuer', verbose_name='Организация', null=True, blank=True, on_delete=SET_NULL)
    award_level = IntegerField(verbose_name='Уровень награды', choices=AWARD_LEVEL, default=0)

    class Meta:
        verbose_name = 'Награда'
        verbose_name_plural = 'Награды'

    def __str__(self):
        return self.award_name


class EmployeeAward(Model):
    employee = ForeignKey(Teacher, verbose_name='Сотрудник', db_index=True, on_delete=CASCADE)
    award = ForeignKey('Award', verbose_name='Награда', on_delete=CASCADE)
    award_date = YearField(verbose_name='Дата нагрждения')

    class Meta:
        verbose_name = 'Награда сотрудника'
        verbose_name_plural = 'Награды сотрудников'

    def __str__(self):
        return self.employee.FIO + '-' + self.award.award_name


class AwardType(Model):
    name = CharField(max_length=250, verbose_name='Тип награды', db_index=True)

    class Meta:
        verbose_name = 'Тип награды'
        verbose_name_plural = 'Типы наград'

    def __str__(self):
        return self.name


class Issuer(Model):
    name = CharField(verbose_name='Наименование организации', max_length=250, db_index=True)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.name
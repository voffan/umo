from django.forms import Form, ModelForm, formset_factory, Textarea, CharField, IntegerField, ChoiceField, RadioSelect

from rpd.models import DisciplineResult, Basement, RPDDisciplineContent, RPDDisciplineContentHours, ClassType, \
    PracticeDescription, WorkType, DisciplineRating, MarkScale, FOS, ELibrary, Bibliography, Language, PracticeType
from umo.models import Semester, Discipline, ExamMarks, EduProgram, Kafedra, Control, Competency, CompetencyIndicator


class Result(ModelForm):
    class Meta:
        model = DisciplineResult
        fields = [
            'competency',
            'indicator',
            'skill',
            'judging',
        ]
        labels = {
            'competency': 'Компетенция',
            'indicator': 'Индикатор компетенции',
            'skill': 'Планируемые результаты',
            'judging': 'Оценочные средства',
        }


class Base(ModelForm):
    class Meta:
        model = Basement
        fields = [
            'discipline',
            'base',
        ]
        labels = {
            'discipline': 'Дисциплина',
            'base': 'Базовые знания',
        }


class HoursDistribution(ModelForm):
    class Meta:
        model = RPDDisciplineContentHours
        fields = [
            'content',
            'hours_type',
            'hours',
        ]
        labels = {
            'content': 'Тема',
            'hours_type': 'Тип работы',
            'hours': 'Кол-во часов',
        }


class DiscContent(ModelForm):
    class Meta:
        model = RPDDisciplineContent
        fields = [
            'theme',
            'content',
        ]
        labels = {
            'theme': 'Тема',
            'content': 'Содержимое',
        }


class SRS_content(ModelForm):
    class Meta:
        model = PracticeDescription
        fields = [
            'theme',
            'class_type',
            'hours',
            'control',
        ]
        labels = {
            'theme': 'Тема',
            'class_type': 'Вид работы',
            'hours': 'Кол-во часов',
            'control': 'Контроль',
        }


class Lab_content(ModelForm):
    class Meta:
        model = PracticeDescription
        fields = [
            'theme',
            'class_type',
            'hours',
            'control',
        ]
        labels = {
            'theme': 'Тема',
            'class_type': 'Вид работы',
            'hours': 'Кол-во часов',
            'control': 'Контроль',
        }


class Disc_Rating(ModelForm):
    class Meta:
        model = DisciplineRating
        fields = [
            'rating_type',
            'semester',
            'work_type',
            'max_points',
            'min_points',
        ]
        labels = {
            'rating_type': 'Вид рейтинговой таблицы',
            'semester': 'Тип практикума',
            'work_type': 'Вид работы',
            'max_points': 'Кол-во часов',
            'min_points': 'Контроль',
        }


class Mark_Scale(ModelForm):
    class Meta:
        model = MarkScale
        fields = [
            'skill',
            'level',
            'criteria',
            'mark',
        ]
        labels = {
            'skill': 'Показатель оценивания',
            'level': 'Уровень освоения',
            'criteria': 'Критерии',
            'mark': 'Оценка',
        }


class FOS_Table(ModelForm):
    class Meta:
        model = FOS
        fields = [
            'skill',
            'theme',
            'sample',
        ]
        labels = {
            'skill': 'Показатель оценивания',
            'theme': 'Тема',
            'sample': 'Образец',
        }


class Bibliography_Table(ModelForm):
    class Meta:
        model = Bibliography
        fields = [
            'reference',
            'elibrary',
            'grif',
            'is_main',
            'count',
        ]
        labels = {
            'reference': 'Библиографическая ссылка',
            'elibrary': 'Электронная литература',
            'grif': 'Наличие грифа',
            'is_main': 'Главная литература',
            'count': 'Кол-во экземпляров',
        }


class RPDProgram(Form):
    goal = CharField(widget=Textarea)
    abstract = CharField(widget=Textarea)
    results = formset_factory(Result)
    basement = formset_factory(Base)
    language = ChoiceField(choices=Language)
    hours_distribution = formset_factory(HoursDistribution)
    theme = formset_factory(DiscContent)
    theme_content = CharField(widget=Textarea)
    education_methods = CharField(widget=Textarea)
    e_method_support = CharField(widget=Textarea)
    srs_content = formset_factory(SRS_content)
    labs_content = formset_factory(Lab_content)
    method_instructions = CharField(widget=Textarea)
    disc_rating = formset_factory(Disc_Rating)
    fos = CharField(widget=Textarea)
    mark_scale = formset_factory(Mark_Scale)
    fos_method = CharField(widget=Textarea)
    fos_table = formset_factory(FOS_Table)
    scaling_method = CharField(widget=Textarea)
    bibl = formset_factory(Bibliography_Table)
    web_resource = CharField(widget=Textarea)
    material = CharField(widget=Textarea)
    it = CharField(widget=Textarea)
    software = CharField(widget=Textarea)
    iss = CharField(widget=Textarea)

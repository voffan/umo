from django.forms import Form, ModelForm, formset_factory, modelformset_factory, Textarea, CharField, IntegerField, \
    ChoiceField, RadioSelect, \
    Select, NumberInput, TextInput, BooleanField, HiddenInput, CheckboxInput

from rpd.models import DisciplineResult, Basement, RPDDisciplineContent, RPDDisciplineContentHours, ClassType, \
    PracticeDescription, WorkType, DisciplineRating, MarkScale, FOS, ELibrary, Bibliography, Language, PracticeType, \
    RPDDiscipline


class Result(ModelForm):
    class Meta:
        model = DisciplineResult
        fields = [
            #'competency.type'
            'competency',
            'indicator',
            'skill',
            'judging',
        ]
        labels = {
            #'competency.type': 'Вид компетенции',
            'competency': 'Компетенция',
            'indicator': 'Индикатор компетенции',
            'skill': 'Планируемые результаты',
            'judging': 'Оценочные средства',
        }
        widgets = {
            #'competency.type': Select(attrs={'class': 'form-control'}),
            'competency': Select(attrs={'class': 'form-control'},),
            'indicator': Select(attrs={'class': 'form-control'}),
            'skill': Textarea(attrs={'class': 'form-control'}),
            'judging': Textarea(attrs={'class': 'form-control'}),
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
        widgets = {
            'discipline': Select(attrs={'class': 'form-control'}),
            'base': Select(attrs={'class': 'form-control'}),
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
            'hours_type': 'Вид учебного занятия',
            'hours': 'Кол-во часов',
        }
        widgets = {
            'content': Select(attrs={'class': 'form-control'}),
            #'content': TextInput(attrs={'class': 'form-control'}),
            'hours_type': Select(attrs={'class': 'form-control'}),
            'hours': NumberInput(attrs={'class': 'form-control'}),
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
        widgets = {
            'theme': TextInput(attrs={'class': 'form-control'}),
            'content': Textarea(attrs={'class': 'form-control'}),
        }


class SRS_content(ModelForm):
    class Meta:
        model = PracticeDescription
        fields = [
            'theme',
            'practice_type',
            'class_type',
            'hours',
            'control',
        ]
        labels = {
            'theme': 'Тема',
            'practice_type' : 'Тип практикума',
            'class_type': 'Вид работы',
            'hours': 'Кол-во часов',
            'control': 'Контроль',
        }
        widgets = {
            'theme': Select(attrs={'class': 'form-control'}),
            'practice_type': Select(attrs={'class': 'form-control'}),
            'class_type': Select(attrs={'class': 'form-control'}),
            'hours': NumberInput(attrs={'class': 'form-control'}),
            'control': Textarea(attrs={'class': 'form-control'}),
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
        widgets = {
            'theme': Select(attrs={'class': 'form-control'}),
            'class_type': Select(attrs={'class': 'form-control'}),
            'hours': NumberInput(attrs={'class': 'form-control'}),
            'control': Textarea(attrs={'class': 'form-control'}),
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
            'semester': 'Семестр',
            'work_type': 'Вид работы',
            'max_points': 'Макс.балл',
            'min_points': 'Мин.балл',
        }
        widgets = {
            'rating_type': Select(attrs={'class': 'form-control'}),
            'semester': Select(attrs={'class': 'form-control'}),
            'work_type': Select(attrs={'class': 'form-control'}),
            'max_points': NumberInput(attrs={'class': 'form-control'}),
            'min_points': NumberInput(attrs={'class': 'form-control'}),
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
        widgets = {
            'skill': Select(attrs={'class': 'form-control'}),
            'level': Select(attrs={'class': 'form-control'}),
            'criteria': Textarea(attrs={'class': 'form-control'}),
            'mark': Select(attrs={'class': 'form-control'},),
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
        widgets = {
            'skill': Select(attrs={'class': 'form-control'}),
            'theme': TextInput(attrs={'class': 'form-control'}),
            'sample': Textarea(attrs={'class': 'form-control'}),
        }


class Bibliography_Table(ModelForm):
    class Meta:
        model = Bibliography
        fields = [
            'reference',
            'elibrary',
            #'grif',
            'is_main',
            'count',
        ]
        labels = {
            'reference': 'Библиографическая ссылка',
            'elibrary': 'Электронная литература',
            #'grif': 'Наличие грифа, вид грифа',
            'is_main': 'Главная литература',
            'count': 'Кол-во экземпляров',
        }
        widgets = {
            'reference': Textarea(attrs={'class': 'form-control'}),
            'elibrary': Select(attrs={'class': 'form-control'}),
            #'grif': Textarea(attrs={'class': 'form-control'}),
            'is_main': CheckboxInput(attrs={'class': 'form-control'}),
            'count': NumberInput(attrs={'class': 'form-control'}),
        }


class RPDProgram(Form):
    goal = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='Цель освоения:')
    abstract = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='Краткое содержание дисциплины:')
    language = ChoiceField(choices=Language, widget=Select(attrs={'class': 'form-control'}), label='Язык:')
    education_methodology = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='В разделе описываются применяемые формы проведения занятий, методы проведения и применяемые учебные технологии:')
    count_e_method_support = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='В разделе раскрывается содержание СРС (аудиторной и внеаудиторной), указываются формы проведения учебных занятий и заданий, формы и методы контроля выполнения СРС, а также тематика письменных работ (рефератов, эссе, докладов, курсовых работ и т.п.), планы самостоятельно выполняемых лабораторных работ и др:')
    methodological_instructions = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='В п.5 включаются методические указания для помощи обучающимся в успешном освоении дисциплины в соответствии с запланированными видами учебной и самостоятельной работы обучающихся, в т.ч., например, методические указания по выполнению курсовых работ/проектов, письменных работ, лабораторных работ и т.п.:')
    fos_fond = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='Раздел должен включать описание показателей (дескрипторов) и критериев оценивания компетенций; описание шкал оценивания примерные  контрольные вопросы и задания (тестовые задания, задачи, кейсы и т.п.), вопросы для подготовки к промежуточной аттестации или иные материалы для оценивания результатов обучения по дисциплине; описание процедуры оценивания.')
    fos_methodology = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='Преподаватель может самостоятельно сформировать наполнение п.6.2. в зависимости от формы проведения промежуточной аттестации')
    scaling_methodology = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='В разделе должны быть представлены методические материалы, определяющие процедуры оценивания знаний, умений, навыков и (или) опыта деятельности, характеризующих этапы формирования компетенций.:')
    web_resource = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='Наименование Интернет-ресурса. Авторы (разработчики) //Ссылка (URL): на Интернет ресурс.:')
    material = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='В разделе указываем необходимое материально-техническое обеспечение по дисциплине (помещения и оборудование) в соответствии с ФГОС ВО, с учетом типов учебных занятий (лекционные, семинарские и т.п.), форм их проведения, а также применяемых информационных и образовательных технологий, в т.ч. ДОТ и электронного обучения.:')
    it = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='Перечень информационных технологий:')
    software = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='Указывается программное обеспечение, на которое университет имеет лицензию и свободно распространяемое программное обеспечение, в том числе отечественного производства.:')
    iss = CharField(widget=Textarea(attrs={'class': 'form-control'}), label='')

    # def save(self):
    #     if self.clean():
    #         new_rpd = RPDDiscipline.objects.create(
    #             goal=self.cleaned_data['goal'],
    #             abstract=self.cleaned_data['abstract'],
    #             language=self.cleaned_data['language'],
    #             education_methodology=self.cleaned_data['education_methodology'],
    #             count_e_method_support=self.cleaned_data['count_e_method_support'],
    #             methodological_instructions=self.cleaned_data['methodological_instructions'],
    #             fos_fond=self.cleaned_data['fos_fond'],
    #             fos_methodology=self.cleaned_data['fos_methodology'],
    #             scaling_methodology=self.cleaned_data['scaling_methodology'],
    #             web_resource=self.cleaned_data['web_resource'],
    #             material=self.cleaned_data['material'],
    #             it=self.cleaned_data['it'],
    #             software=self.cleaned_data['software'],
    #             iss=self.cleaned_data['iss'],
    #     )
    #     return new_rpd


ResultsSet = modelformset_factory(DisciplineResult, form=Result, extra=1)
BasementSet = modelformset_factory(Basement, form=Base, extra=1)
HoursDistributionSet = modelformset_factory(RPDDisciplineContentHours, form=HoursDistribution, extra=1)
ThemeSet = modelformset_factory(RPDDisciplineContent, form=DiscContent, extra=1)
SRSContentSet = modelformset_factory(PracticeDescription, form=SRS_content, extra=1)
LabContentSet = modelformset_factory(PracticeDescription, form=Lab_content, extra=1)
DiscRatingSet = modelformset_factory(DisciplineRating, form=Disc_Rating, extra=1)
MarkScaleSet = modelformset_factory(MarkScale, form=Mark_Scale, extra=1)
FosTableSet = modelformset_factory(FOS, form=FOS_Table, extra=1)
BibliographySet = modelformset_factory(Bibliography, form=Bibliography_Table, extra=1)
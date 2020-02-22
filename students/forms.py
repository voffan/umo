from django.forms import Form, ModelForm, ModelMultipleChoiceField, IntegerField, HiddenInput, ModelChoiceField, BooleanField
from django_select2.forms import ModelSelect2MultipleWidget, ModelSelect2Widget, Select2Widget
from umo.models import Group, CheckPoint, Semester


class GroupsWidget(ModelSelect2MultipleWidget):
    model = Group
    search_fields = ['Name__icontains',]


class GroupWidget(ModelSelect2Widget):
    model = Group
    search_fields = ['Name__icontains',]


class SetProgramToGroupsForm(Form):
    edu_program = IntegerField(widget=HiddenInput(), required=True)
    groups = ModelMultipleChoiceField(widget=GroupsWidget, queryset=Group.objects.all(), required=False, label='Выберите группы')


class GetGroupPointsForm(Form):
    group = ModelChoiceField(widget=GroupWidget, queryset=Group.objects.all(), required=True, label='Группа')
    semester = ModelChoiceField(widget=Select2Widget, queryset=Semester.objects.all().order_by('name'), required=True, label='Семестр')
    checkpoint = ModelChoiceField(widget=Select2Widget, queryset=CheckPoint.objects.all(), required=True, label='Срез')
    excel = BooleanField(required=False, label='Экспортировать в эксель')
    exam = BooleanField(required=False, label='Эзаменационные оценки')




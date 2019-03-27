from django.forms import Form, ModelForm, ModelMultipleChoiceField, IntegerField, HiddenInput
from django_select2.forms import ModelSelect2MultipleWidget
from umo.models import Group, EduProgram


class GroupWidget(ModelSelect2MultipleWidget):
    model = Group
    search_fields = ['Name__icontains',]


class SetProgramToGroupsForm(Form):
    edu_program = IntegerField(widget=HiddenInput(), required=True)
    groups = ModelMultipleChoiceField(widget=GroupWidget, queryset=Group.objects.all(), required=False, label='Выберете группы')




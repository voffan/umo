from django.forms import ModelForm
from django.forms import Form, ModelForm, ModelMultipleChoiceField, IntegerField, HiddenInput, FileField
from django_select2.forms import ModelSelect2MultipleWidget
from umo.models import Discipline, Course, Teacher, DisciplineDetails

class UploadUsersForm(Form):
    #title = CharField(max_length=50, label='название')
    file = FileField(label='файл пользователей')
from django.forms import ModelForm
from django.forms import Form, ModelForm, ModelMultipleChoiceField, IntegerField, HiddenInput, FileField
from django_select2.forms import ModelSelect2MultipleWidget
from hours.models import CourseHours
from django.core.validators import FileExtensionValidator


class UploadFileForm(Form):
    #title = CharField(max_length=50, label='название')
    file = FileField(label='файл', validators=[FileExtensionValidator(allowed_extensions=['xlsx','xls','csv'])])
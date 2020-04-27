from django.forms import Form, ModelForm, ModelMultipleChoiceField, IntegerField, HiddenInput, FileField
from django_select2.forms import ModelSelect2MultipleWidget

from umo.models import Discipline, Course


class UploadFileForm(Form):
    #title = CharField(max_length=50, label='название')
    file = FileField(label='файл')


class SelectTeacher(ModelForm):
    class Meta:
        model = Discipline
        fields = {
            'name',
            #'lecturer'
        }
        labels = {
            'name': ('Дисциплина'),
            #'lecturer': ('Преподаватель')
        }

    def save(self):
        if self.clean():
            discipline = Discipline()
            discipline.name = self.cleaned_data['name']
            #discipline.lecturer = self.cleaned_data['lecturer']
            discipline.save()
            return discipline


class CourseWidget(ModelSelect2MultipleWidget):
    model = Course
    queryset = Course.objects.filter(lecturer__isnull=True, is_finished=False)
    search_fields = ['discipline_detail__discipline__name__icontains', 'group__name__icontains']


class AddSubjectToteacherForm(Form):
    teacher = IntegerField(widget=HiddenInput(), required=True)
    courses = ModelMultipleChoiceField(widget=CourseWidget, queryset=Course.objects.all(), required=False, label='Выберете дисциплины')

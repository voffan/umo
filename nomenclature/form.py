from django import forms
from django.forms import ModelForm
from umo.models import Discipline

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50, label='название')
    file = forms.FileField(label='файл')

class SelectTeacher(ModelForm):
    class Meta:
        model = Discipline
        fields = {
            'Name',
            #'lecturer'
        }
        labels = {
            'Name': ('Дисциплина'),
            #'lecturer': ('Преподаватель')
        }

    def save(self):
        if self.clean():
            discipline = Discipline()
            discipline.Name = self.cleaned_data['Name']
            #discipline.lecturer = self.cleaned_data['lecturer']
            discipline.save()
            return discipline
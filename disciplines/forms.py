from django import forms
from django.forms import ModelForm
from umo.models import Discipline


class AddDisciplineForm(ModelForm):
    class Meta:
        model = Discipline
        fields = [
            'Name',
            'code',
            'program',
            'lecturer',
            'control',
        ]
        labels = {
            'Name': 'Предмет',
            'code': 'Код предмета',
            'program': 'Специализация',
            'lecturer': 'Преподаватель',
            'control': 'Тип контроля',
        }

    def save(self):
        if self.clean():
            discipline = Discipline()
            discipline.Name = self.cleaned_data['Name']
            discipline.code = self.cleaned_data['code']
            discipline.program = self.cleaned_data['program']
            discipline.lecturer = self.cleaned_data['lecturer']
            discipline.control = self.cleaned_data['control']
            discipline.save()
            return discipline


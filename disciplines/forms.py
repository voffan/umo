from django.forms import ModelForm
from umo.models import Discipline


class AddDisciplineForm(ModelForm):
    class Meta:
        model = Discipline
        fields = [
            'name',
            'code',
            'program',
            'lecturer',
            'control',
        ]
        labels = {
            'name': 'Предмет',
            'code': 'Код предмета',
            'program': 'Специализация',
            'lecturer': 'Преподаватель',
            'control': 'Тип контроля',
        }

    def save(self):
        if self.clean():
            discipline = Discipline()
            discipline.name = self.cleaned_data['name']
            discipline.code = self.cleaned_data['code']
            discipline.program = self.cleaned_data['program']
            discipline.lecturer = self.cleaned_data['lecturer']
            discipline.control = self.cleaned_data['control']
            discipline.save()
            return discipline
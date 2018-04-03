from django import forms

from django.contrib.auth import password_validation
from umo.models import Teacher, Position, Zvanie, Kafedra
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class AddTeacherForm(forms.Form):
    FIO = forms.CharField(label='ФИО')
    Position = forms.CharField(label='Должность')
    Zvanie = forms.CharField(label='Звание')


    class Meta:
        model = Teacher, Position, Zvanie, Kafedra

        fields = [
            "FIO",
            "Position",
            "Zvanie",
            "cathedra"
        ]


    def  clean_Zvanie(self):
        data = self.cleaned_data['Zvanie']
        return Zvanie.objects.filter(name__icontains=data).first()

    def clean_Position(self):
        data = self.cleaned_data['Position']
        try:
            position = Position.objects.get(name__icontains=data)
        except Position.DoesNotExist:
            raise forms.ValidationError('Выберете существующую должность!')
        return position


    def save(self):
        if self.clean():
            teacher = Teacher()
            teacher.FIO = self.cleaned_data['FIO']
            teacher.Position = self.cleaned_data['Position']
            teacher.Zvanie = self.cleaned_data['Zvanie']
            teacher.save()
            return  teacher
        #self.add_error('')


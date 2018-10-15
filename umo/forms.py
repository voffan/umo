from django import forms
from django.forms import ModelForm

from django.contrib.auth import password_validation
from umo.models import Teacher, Position, Zvanie, Kafedra, EduProg
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class AddTeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'FIO',
            'Position',
            'Zvanie',
            'cathedra',
            'user'
        ]
        labels = {
            'FIO': _('ФИО'),
            'Position': _('Должность'),
            'Zvanie': _('Звание'),
            'cathedra': _('Кафедра'),
        }


    def save(self):
        if self.clean():
            teacher = Teacher()
            teacher.FIO = self.cleaned_data['FIO']
            teacher.Position = self.cleaned_data['Position']
            teacher.Zvanie = self.cleaned_data['Zvanie']
            teacher.cathedra = self.cleaned_data['cathedra']
            teacher.save()
            return  teacher
        #self.add_error('')


class EditTeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'FIO',
            'Position',
            'Zvanie',
            'cathedra'
        ]
        labels = {
            'FIO': _('ФИО'),
            'Position': _('Должность'),
            'Zvanie': _('Звание'),
            'cathedra': _('Кафедра')
        }

    def edit(self):

         if self.clean():
            teacher = Teacher()
            teacher.FIO = self.cleaned_data['FIO']
            teacher.Position = self.cleaned_data['Position']
            teacher.Zvanie = self.cleaned_data['Zvanie']
            teacher.cathedra = self.cleaned_data['cathedra']
            teacher.save()
            return teacher
from django import forms
from django.forms import ModelForm

from django.contrib.auth import password_validation
from umo.models import Teacher, Position, Kafedra, EduProg
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm


class AddTeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'FIO',
            'position',
            'zvanie',
            'cathedra',
            'user'
        ]
        labels = {
            'FIO': _('ФИО'),
            'position': _('Должность'),
            'zvanie': _('Звание'),
            'cathedra': _('Кафедра'),
        }


    def save(self):
        if self.clean():
            teacher = Teacher()
            teacher.FIO = self.cleaned_data['FIO']
            teacher.position = self.cleaned_data['position']
            teacher.zvanie = self.cleaned_data['zvanie']
            teacher.cathedra = self.cleaned_data['cathedra']
            teacher.save()
            return  teacher
        #self.add_error('')


class EditTeacherForm(ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'FIO',
            'position',
            'zvanie',
            'cathedra'
        ]
        labels = {
            'FIO': _('ФИО'),
            'position': _('Должность'),
            'zvanie': _('Звание'),
            'cathedra': _('Кафедра')
        }

    def edit(self):

         if self.clean():
            teacher = Teacher()
            teacher.FIO = self.cleaned_data['FIO']
            teacher.position = self.cleaned_data['position']
            teacher.zvanie = self.cleaned_data['zvanie']
            teacher.cathedra = self.cleaned_data['cathedra']
            teacher.save()
            return teacher

from datetime import datetime

from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group as auth_groups
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import login, update_session_auth_hash
from django.core.validators import validate_email
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import ModelForm, CharField, ValidationError, PasswordInput, HiddenInput
from openpyxl import Workbook
from openpyxl.styles import PatternFill, Border, Alignment, Protection, Font, Side

import synch.models as sync_models
import rpd.forms as forms
from django.forms import formset_factory
from django.shortcuts import get_object_or_404

from nomenclature.form import AddSubjectToteacherForm
from rpd.models import RPDDiscipline, DisciplineResult, Basement, RPDDisciplineContentHours, RPDDisciplineContent, \
    PracticeDescription, DisciplineRating, MarkScale, FOS, Bibliography
from umo.models import (Teacher, Group, GroupList, Synch, Year, EduProgram, Student, Discipline, CheckPoint, Control,
                        DisciplineDetails, BRSpoints, EduPeriod, ExamMarks, Exam, Course, Person)


def index(request):
    if auth_groups.objects.get(name='teacher') in request.user.groups.all():
        return redirect('disciplines:mysubjects')
    else:
        return redirect('disciplines:disciplines_list')


# Create your views here.
class RPDList(ListView):
    template_name = 'rpd_list.html'
    context_object_name = 'list'

    def get_queryset(self):
        return RPDDiscipline.objects.all()


def rpd_create(request, rpddiscipline_id):
    discipline = RPDDiscipline.objects.filter(id=rpddiscipline_id).first()
    if request.method == 'POST':
        form = forms.RPDProgram(request.POST)
        results = forms.ResultsSet(request.POST)
        basement = forms.BasementSet(request.POST)
        hours_distribution = forms.HoursDistributionSet(request.POST)
        theme = forms.ThemeSet(request.POST)
        srs_content = forms.SRSContentSet(request.POST)
        labs_content = forms.LabContentSet(request.POST)
        disc_rating = forms.DiscRatingSet(request.POST)
        mark_scale = forms.MarkScaleSet(request.POST)
        fos_table = forms.FosTableSet(request.POST)
        bibl = forms.BibliographySet(request.POST)
        bibl2 = forms.BibliographySet(request.POST)
    else:
        data = {'goal': discipline.goal,
                'abstract': discipline.abstract,
                'language': discipline.language,
                'education_methodology': discipline.education_methodology,
                'count_e_method_support': discipline.count_e_method_support,
                'methodological_instructions': discipline.methodological_instructions,
                'fos_fond': discipline.fos_fond,
                'fos_methodology': discipline.fos_methodology,
                'scaling_methodology': discipline.scaling_methodology,
                'web_resource': discipline.web_resource,
                'material': discipline.material,
                'it': discipline.it,
                'software': discipline.software,
                'iss': discipline.iss
                }
        form = forms.RPDProgram(data)
        results = forms.ResultsSet(queryset=DisciplineResult.objects.filter(rpd__id=rpddiscipline_id))
        basement = forms.BasementSet(queryset=Basement.objects.filter(id=rpddiscipline_id))
        hours_distribution = forms.HoursDistributionSet(queryset=RPDDisciplineContentHours.objects.filter(id=rpddiscipline_id))
        theme = forms.ThemeSet(queryset=RPDDisciplineContent.objects.filter(id=rpddiscipline_id))
        srs_content = forms.SRSContentSet(queryset=PracticeDescription.objects.filter(id=rpddiscipline_id))
        labs_content = forms.LabContentSet(queryset=PracticeDescription.objects.filter(id=rpddiscipline_id))
        disc_rating = forms.DiscRatingSet(queryset=DisciplineRating.objects.filter(rpd__id=rpddiscipline_id))
        mark_scale = forms.MarkScaleSet(queryset=MarkScale.objects.filter(rpd__id=rpddiscipline_id))
        fos_table = forms.FosTableSet(queryset=FOS.objects.filter(rpd__id=rpddiscipline_id))
        bibl = forms.BibliographySet(queryset=Bibliography.objects.filter(rpd__id=rpddiscipline_id, is_main=True))
        bibl2 = forms.BibliographySet(queryset=Bibliography.objects.filter(rpd__id=rpddiscipline_id, is_main=False ))
    return render(request, 'rpd.html', context={'discipline': discipline, 'form': form, 'results': results, 'basement': basement,
                                                'hours_distribution': hours_distribution, 'theme': theme, 'srs_content': srs_content,
                                                'labs_content': labs_content, 'disc_rating': disc_rating, 'mark_scale': mark_scale,
                                                'fos_table': fos_table, 'bibl': bibl, 'bibl2': bibl2})


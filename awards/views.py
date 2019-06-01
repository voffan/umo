from django.forms import Form, ModelForm
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, request
from .models import Award, AwardType, EmployeeAward, Issuer
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django_select2.forms import Select2Widget, ModelSelect2Widget
from umo.models import Teacher

from django.contrib.auth.decorators import permission_required

# Create your views here.


def index(request):
    return redirect('awards:list_employee_awards')


class EmployeeAwardsList(ListView):
    template_name = 'awards/employee_awards.html'
    model = EmployeeAward
    context_object_name = 'employee_awards'

    # def get_queryset(self):
    #     # return EmployeeAward.objects.filter(self.model.award.award_level,award__award_level__isnull=self.request.POST('award_level'))
    #     # return EmployeeAward.objects.filter(award__award_level=self.request.POST['award_level'])
    #     # return EmployeeAward.objects.filter(award__award_level=2)
    #     pass
    #
    # def get_context_data(self, **kwargs):
    #     context = super(EmployeeAwardsList, self).get_context_data(**kwargs)
    #     award = Award.objects.last()
    #     if award is not None:
    #         context['award_level'] = str(award.award_level)
    #     else:
    #         context['award_level'] = 'нет'
    #     return context


# class EmployeeAwardsListView(EmployeeAwardsList):
#     pass


class EmployeeWidget(ModelSelect2Widget):
    model = Teacher
    search_fields = ['FIO__icontains',]


class AwardWidget(ModelSelect2Widget):
    model = Award
    search_fields = ['award_name__icontains',]


class EmployeeAwardForm(ModelForm):
    class Meta:
        model = EmployeeAward
        fields = ['employee', 'award', 'award_date']
        widgets = {
            'employee': EmployeeWidget(),
            'award': AwardWidget(),
        }


class EmployeeAwardsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'awards.add_employeeaward'
    template_name = 'awards/employee_award_add.html'
    success_url = reverse_lazy('awards:list_employee_awards')
    form_class = EmployeeAwardForm


class EmployeeAwardsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'awards.change_employeeaward'
    template_name = 'awards/employee_award_update.html'
    success_url = reverse_lazy('awards:list_employee_awards')
    form_class = EmployeeAwardForm
    model = EmployeeAward


class EmployeeAwardsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'awards.delete_employeeaward'
    model = EmployeeAward
    success_url = reverse_lazy('awards:list_employee_awards')
    template_name = 'awards/employee_award_delete.html'


# def employee_award_list(request):
#     employee_awards = EmployeeAward.objects.all()
#     return render(request, 'awards/employee_awards.html', {'employee_awards_list': employee_awards})


class AwardsList(PermissionRequiredMixin, ListView):
    permission_required = 'awards.view_award'
    template_name = 'awards/awards_list.html'
    model = Award


class IssuerWidget(ModelSelect2Widget):
    model = Issuer
    search_fields = ['name__icontains',]


class AwardForm(ModelForm):
    class Meta:
        model = Award
        fields = ['award_type', 'award_name', 'award_level', 'issuer']
        widgets = {
            'issuer': IssuerWidget(),
        }


class AwardsCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'awards.add_award'
    template_name = 'awards/awards_create.html'
    success_url = reverse_lazy('awards:list_awards')
    form_class = AwardForm


class AwardsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'awards.change_award'
    template_name = 'awards/awards_edit.html'
    success_url = reverse_lazy('awards:list_awards')
    form_class = AwardForm
    model = Award


class AwardsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'awards.delete_award'
    model = Award
    success_url = reverse_lazy('awards:list_awards')
    template_name = 'awards/awards_delete.html'

# def award_list(request):
#     awards = Award.objects.all()
#     return render(request, 'awards/awards_list.html', {'awards_list': awards})


class IssuersList(PermissionRequiredMixin, ListView):
    permission_required = 'awards.view_issuer'
    template_name = 'awards/issuer_list.html'
    model = Issuer


class IssuerCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'awards.add_issuer'
    template_name = 'awards/issuer_create.html'
    success_url = reverse_lazy('awards:list_issuers')
    model = Issuer
    fields = ['name']


class IssuerUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'awards.change_issuer'
    template_name = 'awards/issuer_edit.html'
    success_url = reverse_lazy('awards:list_issuers')
    model = Issuer
    fields = ['name']


class IssuerDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'awards.delete_issuer'
    model = Issuer
    success_url = reverse_lazy('awards:list_issuers')
    template_name = 'awards/issuer_delete.html'


# def issuer_list(request):
#     issuer = Issuer.objects.all()
#     return render(request, 'awards/issuer_list.html', {'issuers_list': issuer})
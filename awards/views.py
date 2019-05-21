from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Award, AwardType, EmployeeAward, Issuer
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import permission_required

# Create your views here.


def index(request):
    return redirect('awards:list_employee_awards')


class EmployeeAwardsList(ListView):
    template_name = 'awards/employee_awards.html'
    model = EmployeeAward


class EmployeeAwardsCreate(CreateView):
    template_name = 'awards/employee_award_add.html'
    success_url = reverse_lazy('awards:list_employee_awards')
    model = EmployeeAward
    fields = ['employee', 'award', 'award_date']


class EmployeeAwardsUpdate(UpdateView):
    template_name = 'awards/employee_award_update.html'
    success_url = reverse_lazy('awards:list_employee_awards')
    model = EmployeeAward
    fields = ['employee', 'award', 'award_date']


class EmployeeAwardsDelete(DeleteView):
    model = EmployeeAward
    success_url = reverse_lazy('awards:list_employee_awards')
    template_name = 'awards/employee_award_delete.html'


def employee_award_list(request):
    employee_awards = EmployeeAward.objects.all()
    return render(request, 'awards/employee_awards.html', {'employee_awards_list': employee_awards})


class AwardsList(ListView):
    template_name = 'awards/awards_list.html'
    model = Award


class AwardsCreate(CreateView):
    template_name = 'awards/awards_create.html'
    success_url = reverse_lazy('awards:list_awards')
    model = Award
    fields = ['award_type', 'award_name', 'issuer']


class AwardsUpdate(UpdateView):
    template_name = 'awards/awards_edit.html'
    success_url = reverse_lazy('awards:list_awards')
    model = Award
    fields = ['award_type', 'award_name', 'issuer']


class AwardsDelete(DeleteView):
    model = Award
    success_url = reverse_lazy('awards:list_awards')
    template_name = 'awards/awards_delete.html'

def award_list(request):
    awards = Award.objects.all()
    return render(request, 'awards/awards_list.html', {'awards_list': awards})


class IssuersList(ListView):
    template_name = 'awards/issuer_list.html'
    model = Issuer

class IssuerCreate(CreateView):
    template_name = 'awards/issuer_create.html'
    success_url = reverse_lazy('awards:list_issuers')
    model = Issuer
    fields = ['name']

class IssuerUpdate(UpdateView):
    template_name = 'awards/issuer_edit.html'
    success_url = reverse_lazy('awards:list_issuers')
    model = Issuer
    fields = ['name']

class IssuerDelete(DeleteView):
    model = Issuer
    success_url = reverse_lazy('awards:list_issuers')
    template_name = 'awards/issuer_delete.html'


def issuer_list(request):
    issuer = Issuer.objects.all()
    return render(request, 'awards/issuer_list.html', {'issuers_list': issuer})
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import render, redirect
from umo.models import Discipline
from disciplines.forms import AddDisciplineForm
from django.http import HttpResponseRedirect


# Create your views here.
def list(request):
    all = Discipline.objects.all()
    return render(request, 'disciplines.html', {'disciplines': all})


def add_discipline(request):
    if request.method == 'POST':
        form = AddDisciplineForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/disciplines/list/')
        return render(request, 'disciplines_form.html', {'form': form})
    form = AddDisciplineForm()
    return render(request, 'disciplines_form.html', {'form': form})
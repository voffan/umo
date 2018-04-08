from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import render
from umo.models import Discipline
from disciplines.forms import AddDisciplineForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse

# Create your views here.
# def list(request):
#     all = Discipline.objects.all()
#     return render(request, 'disciplines.html', {'disciplines': all})


class DisciplineList(ListView):
    template_name = 'disciplines.html'
    context_object_name = 'discipline_list'

    def get_queryset(self):
        return Discipline.objects.all()


class DisciplineCreate(CreateView):
    template_name = 'disciplines_form.html'
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


class DisciplineDetail(DetailView):
    template_name = 'disciplines_detail.html'
    model = Discipline
    fields = [
        'Name',
        'code',
        'program',
        'lecturer',
        'control',
    ]


class DisciplineUpdate(UpdateView):
    template_name = 'disciplines_update.html'
    success_url = reverse_lazy('disciplines:disciplines_list')
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


class DisciplineDelete(DeleteView):
    template_name = 'disciplines_delete.html'
    model = Discipline
    success_url = reverse_lazy('disciplines:disciplines_list')


def add_discipline(request):
    if request.method == 'POST':
        form = AddDisciplineForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/disciplines/list/')
        return render(request, 'disciplines_form.html', {'form': form})
    form = AddDisciplineForm()
    return render(request, 'disciplines_form.html', {'form': form})


def delete(request):
    if request.method == 'POST':
        discipline_ = Discipline.objects.get(pk=request.POST['discipline'])
        discipline_.delete()
        return HttpResponseRedirect(reverse('disciplines:disciplines_list'))

from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from umo.models import Discipline, DisciplineDetails
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from disciplines.forms import AddDisciplineForm
from django.http import HttpResponseRedirect, HttpResponse


# Create your views here.
# def list(request):
#     all = Discipline.objects.all()
#     return render(request, 'disciplines.html', {'disciplines': all})


# def add_discipline(request):
#     if request.method == 'POST':
#         form = AddDisciplineForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/disciplines/list/')
#         return render(request, 'disciplines_form.html', {'form': form})
#     form = AddDisciplineForm()
#     return render(request, 'disciplines_form.html', {'form': form})


class DisciplineList(ListView):
    template_name = 'disciplines.html'
    context_object_name = 'discipline_list'

    def get_queryset(self):
        return Discipline.objects.all()


class DisciplineCreate(CreateView):
    template_name = 'disciplines_form.html'
    success_url = reverse_lazy('disciplines:details_add')
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


class DisciplineDelete(DeleteView):
    template_name = 'disciplines_delete.html'
    model = Discipline
    success_url = reverse_lazy('disciplines:disciplines_list')


class DisciplineDetail(DetailView):
    template_name = 'disciplines_detail.html'
    model = DisciplineDetails
    context_object_name = 'discipline_detail'


def discipline_detail(request, pk):
    if request.method == 'POST':
        pass
    subject_ = Discipline.objects.get(id=pk)
    details_ = DisciplineDetails.objects.get(subject__id=subject_.id)
    form = DisciplineDetail(object=details_)
    return render(request, 'disciplines_detail.html', {'form': form})


class DetailsCreate(CreateView):
    template_name = 'details_form.html'
    model = DisciplineDetails
    success_url = reverse_lazy('disciplines:disciplines_list')
    fields = [
        'subject',
        'Credit',
        'Lecture',
        'Practice',
        'Lab',
        'KSR',
        'SRS',
        'semestr',
    ]
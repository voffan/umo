from django.views.generic import ListView, CreateView, UpdateView, DetailView
from umo.models import Discipline, DisciplineDetails
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from disciplines.forms import AddDisciplineForm


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


def discipline_delete(request):
    if request.method == 'POST':
        discipline_ = Discipline.objects.get(pk=request.POST['discipline'])
        discipline_.delete()
        return HttpResponseRedirect(reverse('disciplines:disciplines_list'))
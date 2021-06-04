from django.contrib import auth
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import Group as auth_groups
from django.http import HttpResponseRedirect

from loginsys.forms import RegistrationForm


def login(request):
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if auth_groups.objects.get(name='teacher') in request.user.groups.all():
                return HttpResponseRedirect(reverse('disciplines:mysubjects'))
            elif auth_groups.objects.get(name='student') in request.user.groups.all():
                return HttpResponseRedirect(reverse('students:subjects'))
            else:
                return HttpResponseRedirect(reverse('disciplines:disciplines_list'))
        else:
            args['login_error'] = "Внимание, вход на сайт не был произведен. " \
                                  "Возможно, вы ввели неверное имя пользователя или пароль."
            return render(request, 'login.html', args)
    else:
        return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    args = {}
    args['form'] = RegistrationForm()
    if request.POST:
        newuser_form = RegistrationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return render(request, 'register_success.html')
        else:
            args['form'] = newuser_form
    return render(request, 'register.html', args)
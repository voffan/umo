from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import requires_csrf_token, csrf_exempt
from loginsys.forms import RegistrationForm

def login(request):
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/teacher/')
        else:
            args['login_error'] = "Внимание, вход на сайт не был произведен. Возможно, вы ввели неверное имя пользователя или пароль."
            return render(request, 'login.html', args)

    else:
        return render(request, 'login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("login.html")

def register(request):
    args = {}
    args['form'] = RegistrationForm()
    if request.POST:
        newuser_form = RegistrationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            return HttpResponseRedirect('/auth/register_success/')
        else:
            args['form'] = newuser_form
    return render(request, 'register.html', args)

def register_success(request):
    args = {}
    return render(request, 'register_success.html', args)

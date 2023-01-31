from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from . import forms
from django.contrib import auth


# Create your views here.

def main(request:HttpRequest,*args, **kwargs):
    return render(request, "main.html")

def start(request:HttpRequest, *args, **kwargs):
    return render(request, "test_start.html")

def signup(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, template_name="test_success.html")
        else:
            return redirect('wapl:signup')
    else:
        form = forms.SignupForm()
        context = {
            'form': form,
        }
        return render(request, template_name='test_signup.html', context=context)

def login(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print("로그인 성공~~~~~~~~~")
            return redirect('wapl:start')
        else:
            context = {
                'form': form,
            }
            return render(request, template_name='test_login.html', context=context)
    else:
        form = forms.LoginForm()
        context = {
            'form': form,
        }
        return render(request, template_name='test_login.html', context=context)

def logout(request:HttpRequest, *args, **kwargs):
    auth.logout(request)
    return redirect('wapl:start')

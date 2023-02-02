from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from . import forms
from django.contrib import auth
from server.apps.wapl.models import Comment
from django.core import serializers

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
            return redirect('wapl:login')
        else:
            return redirect('wapl:signup')
    else:
        form = forms.SignupForm()
        context = {
            'form': form,
        }
        return render(request, template_name='signup.html', context=context)

def login(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            print("로그인 성공~~~~~~~~~")
            return redirect('wapl:main')
        else:
            context = {
                'form': form,
            }
            return render(request, template_name='login.html', context=context)
    else:
        form = forms.LoginForm()
        context = {
            'form': form,
        }
        return render(request, template_name='login.html', context=context)

def logout(request:HttpRequest, *args, **kwargs):
    auth.logout(request)
    return redirect('wapl:start')

@csrf_exempt
def view_plan(request):
  req = json.loads(request.body)
  year = req['year']
  month = req['month'] + 1


  plans = Plan.objects.filter(startTime__month=month)
  username = request.user.username;

  #1. plans 객체를 필터링 해서 json 직렬화 하여 리턴
  plans = serializers.serialize('json', plans) # => plans == string
  return JsonResponse({'plans': plans, 'username':username})

  
@csrf_exempt
def view_explan(request):
    req = json.loads(request.body)
    year = req['year']
    month = req['month']
    day = req['day']

    plans = Plan.objects.filter(startTime__year=year,startTime__month=month,startTime__day=day);
    plans = plans.order_by('startTime');
    username = request.user.username;

    plans = serializers.serialize('json', plans) 
    return JsonResponse({'plans': plans, 'username':username})

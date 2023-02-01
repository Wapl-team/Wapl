from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Plan
import json
from django.core import serializers
from . import forms
from django.contrib import auth
from server.apps.wapl.models import Comment
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm


@csrf_exempt
def main(request:HttpRequest,*args, **kwargs):
  plans = Plan.objects.all()
  context = {'plans': plans}
  return render(request, "main.html", context=context)


def comment(request:HttpRequest, *args, **kwargs):
    
    if request.method == "POST":
        Comment.objects.create(
            content=request.POST["content"],
            user=request.POST["user"],
            plan_post=request.POST["plan_post"],
        )
        return redirect('wapl:comment') 
    
    comments = Comment.objects.all()
    
    context = {
        "comments" : comments,
    }
    
    return render(request, "test__comment.html", context=context)

def comment_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        comment = Comment.objects.get(id=pk)
        comment.delete()
    return redirect('wapl:comment')


#일정 생성 함수
#POST로 넘어온 데이터로 newPlan 모델 객체 생성 및 저장
#리턴하는 값 X (js에서 작업 필요)
@csrf_exempt
def create(request, *args, **kwargs):
  if request.method == 'POST':
    req = json.loads(request.body)
    newPlan = Plan(startTime = req['startTime'], endTime = req['endTime'], location = req['location'], title = req['title'], content = req['content'])
    newPlan.save()
    context = {'newPlan': newPlan}
    return JsonResponse({})


#일정 수정 함수
#POST로 넘어온 데이터로 updatedPlan 모델 객체 저장
#리턴하는 값 X (js에서 작업 필요)
@csrf_exempt
def update(request, *args, **kwargs):
  if request.method == 'POST':
    req = json.loads(request.body)
    pk = req['id']
    updatedPlan = Plan.objects.all().get(id=pk)
    updatedPlan.startTime = req['startTime']
    updatedPlan.endTime = req['endTime']
    updatedPlan.location = req['location']
    updatedPlan.title = req['title']
    updatedPlan.content = req['content']
    updatedPlan.save()
    context = {'updatedPlan': updatedPlan}
    return JsonResponse({})


#일정 생성 함수
#POST로 넘어온 데이터로 newPlan 모델 객체 생성 및 저장
#리턴하는 값 X (js에서 작업 필요)
@csrf_exempt
def retrieve(request, *args, **kwargs):
  plans = serializers.serialize('json', Plan.objects.all())
  return JsonResponse({'plans': plans})


#일정 삭제 함수
#POST로 넘어온 id값으로 객체 삭제
#리턴하는 값 X (js에서 작업 필요)
@csrf_exempt
def delete(request, *args, **kwargs):
  if request.method == 'POST':
    pk = json.loads(request.body)['id']
    Plan.objects.all().get(id=pk).delete()
  return JsonResponse({})
  

#일정 상세보기 함수
#delete 테스트를 위해 임시로 넣은 함수
def detail(request, pk, *args, **kwargs):
  plan = Plan.objects.all().get(id=pk)
  
  startTime = str(plan.startTime)
  print(startTime.split(" "))
  context = {'plan': plan}
  return render(request, 'test_detail.html', context=context)

def start(request:HttpRequest, *args, **kwargs):
    return render(request, "test_start.html")

def signup(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('wapl:main')
        else:
            return redirect('wapl:signup')
    else:
        return render(request, template_name='signup.html')

def login(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = forms.LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('wapl:main')
        else:
            return render(request, template_name='login.html')
    else:
        return render(request, template_name='login.html')

def logout(request:HttpRequest, *args, **kwargs):
    auth.logout(request)
    return redirect('wapl:start')

def view_plan(request):
  req = json.loads(request.body)
  year = req['year']
  month = req['month'] + 1

# 프로필 업데이트 함수
def profile(request:HttpRequest, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("wapl:login")

    if request.method == "POST":
        form = forms.EditProfileForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            form.save()
            return render(request, 'profile.html')
        else:
            return redirect('wapl:profile')
    else:
        context = {
            'user': request.user,
        }
        return render(request, 'profile.html', context=context)

def update_password(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("wapl:login")

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('wapl:profile')
        else:
            redirect('wapl:update_password')
    else:
        return render(request, 'update_password.html')
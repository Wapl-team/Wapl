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

from server.apps.wapl.models import Comment, Meeting


@csrf_exempt
def main(request:HttpRequest,*args, **kwargs):
  plans = Plan.objects.all()
  meetings = Meeting.objects.all()
  
  context = {
            'plans' : plans,
            'meetings' : meetings, }
  
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

# 미팅 pt 입니다--------------------------------------------------------------

def meeting_create(request:HttpRequest, *args, **kwargs):
    
    if request.method == 'POST':
        Meeting.objects.create(
            
        meeting_name = request.POST["meeting_name"],
        content = request.POST["content"],
        category = request.POST["category"],
        user = request.POST["user"],
        plan = request.POST["plan"],
        
        )
        return redirect('wapl:main') 

    context = {}
    
    return render(request, "test_meeting_create.html", context=context)

def meeting_detail(request:HttpRequest, pk, *args, **kwargs):
    meeting = Meeting.objects.get(id=pk)
    context = {
        "meeting" : meeting
    }
    return render(request, "test_meeting_detail.html", context=context)

def meeting_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        meeting = Meeting.objects.get(id=pk)
        meeting.delete()
        return redirect('wapl:main')

# ------------------------------------------------------------------------------

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

def view_plan(request):
  req = json.loads(request.body)
  year = req['year']
  month = req['month'] + 1

  
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Plan, Comment, Meeting
import json
from django.core import serializers
from datetime import datetime
from . import forms
from django.contrib import auth
from .validators import *

# 인자로 넘어온 기준으로 일정을 필터링 하는 함수
# 필터 기준(인자): user 객체, 모임 이름, 얀도, 월
# 리턴: Plan 모델 QuerySet
def findPlan(user, category, year, month):  
  meetingObj = Meeting.objects.all().filter(user=user).get(meeting_name=category)
  data = Plan.objects.all().filter(meeting=meetingObj, startTime__month = month, startTime__year = year)
  
  return data


# main 페이지 접속 시 실행 함수
# 디폴트 달력은 개인 달력
@csrf_exempt
def main(request:HttpRequest,*args, **kwargs):
  category = '개인' # 디폴트가 개인 => 향후 수정 가능

  plans = findPlan(request.user, category, datetime.now().year, datetime.now().month)
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







# 일정 생성 함수
# POST로 넘어온 데이터로 newPlan 모델 객체 생성 및 저장
# 리턴하는 값: 에러 메세지 -> 딕셔너리 형태 {key: (Plan 모델 필드)_err, value: (에러 메세지)}
# ex) 날짜 에러인 경우 -> err_msg['time_err'] == "종료 시간이 시작 시간보다 이전일 수 없습니다."
@csrf_exempt
def create(request, *args, **kwargs):
  if request.method == 'POST':
    req = json.loads(request.body)
    
    result, err_msg = validate_plan(startTime = req['startTime'], endTime = req['endTime'], title = req['title'])
    if result:
      newPlan = Plan(startTime = req['startTime'], endTime = req['endTime'], location = req['location'], title = req['title'], content = req['content'])
      newPlan.save()
    
    return JsonResponse(err_msg)


# 일정 수정 함수
# POST로 넘어온 데이터로 updatedPlan 모델 객체 저장
# 리턴하는 값: 에러 메세지 -> 딕셔너리 형태 {key: (Plan 모델 필드)_err, value: (에러 메세지)}
# ex) 날짜 에러인 경우 -> err_msg['time_err'] == "종료 시간이 시작 시간보다 이전일 수 없습니다."
@csrf_exempt
def update(request, *args, **kwargs):
  if request.method == 'POST':
    
    req = json.loads(request.body)
    result, err_msg = validate_plan(startTime = req['startTime'], endTime = req['endTime'], title = req['title'])
    if result:
      pk = req['id']
      updatedPlan = Plan.objects.all().get(id=pk)
      updatedPlan.startTime = req['startTime']
      updatedPlan.endTime = req['endTime']
      updatedPlan.location = req['location']
      updatedPlan.title = req['title']
      updatedPlan.content = req['content']
      updatedPlan.save()

    return JsonResponse(err_msg)

# 일정 삭제 함수
# POST로 넘어온 id값으로 객체 삭제
# 리턴하는 값 X
@csrf_exempt
def delete(request, *args, **kwargs):
  if request.method == 'POST':
    pk = json.loads(request.body)['id']
    Plan.objects.all().get(id=pk).delete()
  return JsonResponse({})
  

# 일정 상세보기 함수
# delete 테스트를 위해 임시로 넣은 함수
def detail(request, pk, *args, **kwargs):
  plan = Plan.objects.all().get(id=pk)
  
  startTime = str(plan.startTime)
  context = {'plan': plan}
  return render(request, 'test_detail.html', context=context)


# 모임 변경 시 실행 함수
# 해당 모임에 존재하는 모든 일정들을 불러와 리턴
# 일정 필터링 순서: 현재 로그인 유저가 소유한 모임인가? -> 유저가 선택한 카테고리인가? -> 해당 모임에 존재하는 일정인가?
@csrf_exempt
def view_plan(request):
  req = json.loads(request.body)
  year = req['year']
  month = req['month'] + 1
  category = req['meeting'] # 화면에서 유저가 선택한 카테고리 이름(meeting_name)을 넘겨야 함
  
  plans = findPlan(request.user, category, year, month)
  
  plans = serializers.serialize('json', plans)
  return JsonResponse({'plans': plans})








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

  
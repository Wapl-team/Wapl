
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
from django.core import serializers
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import random

# main 페이지 접속 시 실행 함수
# 디폴트 달력은 개인 달력
@csrf_exempt
def main(request:HttpRequest,*args, **kwargs):
  meetings = Meeting.objects.all()
  context = {            
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
    category_list = Meeting.MEETING_CHOICE
    context = {
        "category_list":category_list
    }
    
    return render(request, "meeting_create.html", context=context)

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






# 일정 생성 함수
# POST로 넘어온 데이터로 newPlan 모델 객체 생성 및 저장
# 리턴하는 값: 에러 메세지 -> 딕셔너리 형태 {key: (Plan 모델 필드)_err, value: (에러 메세지)}
# ex) 날짜 에러인 경우 -> err_msg['time_err'] == "종료 시간이 시작 시간보다 이전일 수 없습니다."
@csrf_exempt
def create(request, *args, **kwargs):
  if request.method == 'POST':
    req = json.loads(request.body)

    startTime = req['startTime'];
    endTime = req['endTime'];
    result, err_msg = validate_plan(startTime = startTime, endTime = endTime, title = req['title'])
    if result:
        newPlan = Plan(user=request.user, startTime = req['startTime'], endTime = req['endTime'], location = req['location'], title = req['title'], content = req['content'])
        newPlan.save()
    return JsonResponse({'startTime':startTime, 'endTime':endTime, 'err_msg':err_msg, 'userimg':request.user.image.url})


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
  context = {'plan': plan}
  return render(request, 'test_detail.html', context=context)

def start(request:HttpRequest, *args, **kwargs):
    return render(request, "test_start.html")

@csrf_exempt
def signup(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        form = forms.SignupForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            user = form.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('wapl:main')
        else:
            return redirect('wapl:signup')
    else:
        default_image_index = random.randint(1, 4)
        context = {
            'default_src': f'static/default_image/{default_image_index}.png'
        }
        return render(request, template_name='signup.html', context=context)

@csrf_exempt
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

  

@csrf_exempt
def view_plan(request):
  req = json.loads(request.body)
  year = req['year']
  month = req['month'] + 1
  meeting_name = req['meeting'] # 화면에서 유저가 선택한 카테고리 이름(meeting_name)을 넘겨야 함
  username = request.user.username

  if meeting_name == ' ':

    plans = Plan.objects.all().filter(user = request.user, startTime__month = month, startTime__year = year)
  else:
    meetingObj = Meeting.objects.all().filter(user = request.user).get(meeting_name = meeting_name)
    plans = Plan.objects.all().filter(meeting = meetingObj, startTime__month = month, startTime__year = year)
    

  plans = serializers.serialize('json', plans)
  return JsonResponse({'plans': plans, 'username': username})

# if문에 개인달력 출력하는 부분 
# 모델 -> plan 공개여부
# 공유달력 출력 
  
@csrf_exempt
def view_explan(request):
    req = json.loads(request.body)
    year = req['year']
    month = req['month']
    day = req['day']
    meeting_name = req['meetingName']
    meetingObj = Meeting.objects.all().filter(user = request.user).get(meeting_name = meeting_name)
    plans = Plan.objects.all().filter(meeting = meetingObj, startTime__month = month, startTime__year = year, startTime__day = day)
    plans = plans.order_by('startTime')
    username = request.user.username

    plans = serializers.serialize('json', plans) 
    return JsonResponse({'plans': plans, 'username':username})
  

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

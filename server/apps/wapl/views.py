

from django.shortcuts import render, redirect, get_object_or_404

from django.http.request import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PrivatePlan ,PublicPlan, Comment, Meeting
import json
from django.core import serializers
from datetime import date, timedelta, datetime
from . import forms
from django.contrib import auth
from .validators import *
from django.core import serializers
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from itertools import chain
from django.urls import reverse
import random
import uuid
import base64
import codecs

# main 페이지 접속 시 실행 함수
# 디폴트 달력은 개인 달력
# 모임 생성 유저는 자동으로 users에 들어감
@csrf_exempt
def main(request:HttpRequest,*args, **kwargs):
  login_user = request.user
  meetings = login_user.user_meetings.all()
  context = {            
            'meetings' : meetings, 
            'meeting_name': ''}
  
  return render(request, "main.html", context=context)

@csrf_exempt
def meeting_calendar(request, pk, *args, **kwargs):
  login_user = request.user
  cur_meeting = Meeting.objects.all().get(id=pk)
  print(cur_meeting)
  meetings = login_user.user_meetings.all()
  print(meetings)
  
  context = {'cur_meeting': cur_meeting,
             'meetings': meetings}
  return render(request, "meeting_main.html", context=context)




# 미팅 pt 입니다--------------------------------------------------------------
@csrf_exempt
def meeting_create(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        default_image_index = random.randint(1, 4)
        newMeeting = Meeting.objects.create(
        meeting_name = request.POST["meeting_name"],
        content = request.POST["content"],
        owner = request.user,
        category = request.POST["category"],
        invitation_code = generate_invitation_code(),
        image = request.FILES.get("image"),
        default_image = f'/static/default_image/t{default_image_index}.png',
        )
        newMeeting.users.add(request.user)
        
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

def meeting_join(request:HttpRequest, *args, **kwargs):
    if request.method == "POST":
        code = request.POST["code"]
        try:
            meeting = Meeting.objects.get(invitation_code=code)
            meeting.users.add(request.user)
            url = reverse('wapl:meeting_calendar', args=[meeting.id])
            return redirect(url)
        except:
            return redirect('wapl:meeting_join')

    else:
        return render(request, 'meeting_join.html')
    
# 일정+Comment pt 입니다-----------------------------------------------------------------

# 일정 생성 함수
# POST로 넘어온 데이터로 newPlan 모델 객체 생성 및 저장
# 리턴하는 값: 에러 메세지 -> 딕셔너리 형태 {key: (Plan 모델 필드)_err, value: (에러 메세지)}
# ex) 날짜 에러인 경우 -> err_msg['time_err'] == "종료 시간이 시작 시간보다 이전일 수 없습니다."
@csrf_exempt
def create_private_plan(request, *args, **kwargs):
  if request.method == 'POST':
    req = json.loads(request.body)
    startTime = req['startTime']
    endTime = req['endTime']

    # result, err_msg = validate_plan(startTime = startTime, endTime = endTime, title = req['title'])
    # public private 따로 구현 예정
    newPlan = PrivatePlan.objects.create(owner = request.user, startTime = startTime, endTime = endTime, location = req['location'], title = req['title'], content = req['content'])
    

    if request.user.image == "":
        return JsonResponse({'planName': newPlan.title, 'startTime': newPlan.startTime, 'endTime': newPlan.endTime, 'pk': newPlan.id, 'userimg':request.user.default_image})
    else:
        return JsonResponse({'planName': newPlan.title, 'startTime': newPlan.startTime, 'endTime': newPlan.endTime, 'pk': newPlan.id, 'userimg':request.user.image.url})

@csrf_exempt
def create_public_plan(request, *args, **kwargs):
  if request.method == 'POST':
    req = json.loads(request.body)
    startTime = req['startTime'].replace('T',' ')+":00"
    endTime = req['endTime'].replace('T',' ')+":00"
    meeting = Meeting.objects.get(meeting_name=req['meeting_name'])

    # result, err_msg = validate_plan(startTime = startTime, endTime = endTime, title = req['title'])
    newPlan = PublicPlan.objects.create(meetings = meeting, startTime = startTime, endTime = endTime, location = req['location'], title = req['title'], content = req['content'])
    

    if request.user.image == "":
        return JsonResponse({'planName': newPlan.title, 'startTime': newPlan.startTime, 'endTime': newPlan.endTime, 'pk': newPlan.id, 'userimg':request.user.default_image})
    else:
        return JsonResponse({'planName': newPlan.title, 'startTime': newPlan.startTime, 'endTime': newPlan.endTime, 'pk': newPlan.id, 'userimg':request.user.image.url})

# 일정 수정 함수
# POST로 넘어온 데이터로 updatedPlan 모델 객체 저장
# 리턴하는 값: 에러 메세지 -> 딕셔너리 형태 {key: (Plan 모델 필드)_err, value: (에러 메세지)}
# ex) 날짜 에러인 경우 -> err_msg['time_err'] == "종료 시간이 시작 시간보다 이전일 수 없습니다."

def update(request:HttpRequest, pk, *args, **kwargs):
    plan = Plan.objects.get(id=pk)
    plan_sT = plan.startTime.strftime('%Y-%m-%d %H:%M:%S')
    plan_eT = plan.endTime.strftime('%Y-%m-%d %H:%M:%S')
    
    if request.method == "POST":
        plan.startTime = request.POST["startTime"]
        plan.endTime = request.POST["endTime"]
        plan.location = request.POST["location"]
        plan.title = request.POST["title"]
        plan.content = request.POST["content"]
        plan.save()
        
        return redirect('wapl:detail', pk) 
    return render(request, "plan_update.html", {"plan":plan, "plan_sT":plan_sT, "plan_eT":plan_eT})


#일정 생성 함수
#POST로 넘어온 데이터로 newPlan 모델 객체 생성 및 저장
#리턴하는 값 X (js에서 작업 필요)
@csrf_exempt
def retrieve(request, *args, **kwargs):
  plans = serializers.serialize('json', PrivatePlan.objects.all())
  return JsonResponse({'plans': plans})


#일정 삭제 함수
#POST로 넘어온 id값으로 객체 삭제
@csrf_exempt

def delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        plan = Plan.objects.get(id=pk)
        plan.delete()
        return redirect('wapl:main')


#일정 상세보기 함수 + 댓글 생성/리스트 출력까지
def detail(request, pk, *args, **kwargs):
    # plan = Plan.objects.all().get(id=pk)
    plan = get_object_or_404(PrivatePlan, pk=pk)
    
    startTime = str(plan.startTime)
    if request.user.is_authenticated:
        if request.method == "POST":
            Comment.objects.create(
                content=request.POST["content"],
                user=request.user,
                plan_post=plan,
            )
            return redirect('wapl:detail', pk) 
    
    context = {
        "plan": plan,
   }
    return render(request, 'plan_detail.html', context=context)

def public_detail(request, pk, *args, **kwargs):
    # plan = Plan.objects.all().get(id=pk)
    plan = get_object_or_404(PrivatePlan, pk=pk)
    
    startTime = str(plan.startTime)
    if request.user.is_authenticated:
        if request.method == "POST":
            Comment.objects.create(
                content=request.POST["content"],
                user=request.user,
                plan_post=plan,
            )
            return redirect('wapl:detail', pk) 
    
    comments = Comment.objects.all().filter(plan_post=plan)
    context = {
        "plan": plan,
        "comments" : comments,}
    return render(request, 'plan_detail.html', context=context)

def comment_delete(request:HttpRequest, pk, ak, *args, **kwargs):
    if request.method == "POST":
        comment = Comment.objects.get(id=pk)
        comment.delete()
        
    return redirect('wapl:detail', ak)

# -------------------------------------------------------------------------
def start(request:HttpRequest, *args, **kwargs):
    return render(request, "test_start.html")

@csrf_exempt
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
        default_image_index = random.randint(1, 4)
        context = {
            'default_src': f'/static/default_image/{default_image_index}.png'
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

# 모임 별 일정들 union 하는 함수
# 추후 더 좋은 방법 있으면 수정 예정
# 리턴: QuerySet  (objects가 없으면 빈 리스트)
def unionQuerySet(objects):
  data = ''
  cnt = len(objects)
  if cnt > 1:
    data = objects[0].plans.all()
    for i in range(cnt):
      if i <  cnt - 1:
        data = data.union(objects[i+1].plans.all())
  elif cnt == 1:
    data = objects[0].plans.all()
  else:
    data = []
  return data

@csrf_exempt
# 개인달력 출력 
def view_plan(request):
  req = json.loads(request.body)
  year = req['year']
  month = req['month'] 
  login_user = request.user
  
  private_plans = PrivatePlan.objects.filter(owner=login_user, startTime__month__lte=month, endTime__month__gte=month)

  meetings = login_user.user_meetings.all()

  public_plans = []

  meeting_img = {}

  for i in range(len(meetings)) :
     if meetings[i].image == "":
        meeting_img[meetings[i].pk] = meetings[i].default_image
     else:
        meeting_img[meetings[i].pk] = meetings[i].image.url


  for meeting in meetings :
      public_plan = PublicPlan.objects.all().filter(meetings = meeting, startTime__month__lte = month , endTime__month__gte = month)
      public_plans += list(public_plan)


  private_plans = serializers.serialize('json', private_plans)

  public_plans = serializers.serialize('json', public_plans)
  # PrivatePlan에서 owner가 로그인 유저인 Plan 필터링 예정


  if request.user.image == "":
    return JsonResponse({'public_plans': public_plans,
                         'private_plans':private_plans,'userimg':request.user.default_image,
                         'meetingimg':meeting_img})
  else:
    return JsonResponse({'public_plans': public_plans,
                         'private_plans':private_plans, 'userimg':request.user.image.url,
                         'meetingimg':meeting_img})

@csrf_exempt
def view_team_plan(request):
  req = json.loads(request.body)
  year = req['year']
  month = req['month'] + 1
  meeting_pk = req['meetingPK'] # 화면에서 유저가 선택한 모임 pk를 넘겨야 함
  login_user = request.user
  
  meetingObj = Meeting.objects.all().get(id=meeting_pk)
  plans = meetingObj.plans.all()
  plans = serializers.serialize('json', plans)
  if request.user.image == "":
    return JsonResponse({'plans': plans,'userimg':request.user.default_image})
  else:
    return JsonResponse({'plans': plans, 'userimg':request.user.image.url})

# 날짜 클릭 시 호출 함수
# 해당 날짜에 해당하는 일정들 정보를 넘겨줌
# 추후 수정 예정(현재 클릭 불가로 수정X)  
@csrf_exempt
def view_explan(request):
  req = json.loads(request.body)
  year =int(req['year'])
  month = int(req['month'])
  day = int(req['day'])
  login_user = request.user
  meetings = login_user.user_meetings.all()
  today = date(year,month,day)

  private_plans = PrivatePlan.objects.filter(owner = login_user, startTime__lte = today + timedelta(days=1), endTime__gte = today)


  # 여기서 필터링 방법을 아래처럼 해야할 것 같은데 혹시 몰라서 그냥 위처럼 놔둠
  # plans= PrivatePlan.objects.all().filter(owner = user, startTime__lte = today + timedelta(days=1), endTime__gte = today)

  public_plans = []

  meeting_img = {}

  for i in range(len(meetings)) :
     if meetings[i].image == "":
        meeting_img[meetings[i].pk] = meetings[i].default_image
     else:
        meeting_img[meetings[i].pk] = meetings[i].image.url

  for meeting in meetings :
      public_plan = PublicPlan.objects.all().filter(meetings = meeting, startTime__lte = today + timedelta(days=1), endTime__gte = today)
      public_plans += list(public_plan)
    

  private_plans = serializers.serialize('json', private_plans)

  public_plans = serializers.serialize('json', public_plans)

  if request.user.image == "":
      return JsonResponse({'public_plans': public_plans,
                         'private_plans':private_plans,'today': day,'userimg':request.user.default_image,
                         'meetingimg':meeting_img})
  else:
      return JsonResponse({'public_plans': public_plans,
                         'private_plans':private_plans, 'today': day,'userimg':request.user.image.url,
                         'meetingimg':meeting_img})

@csrf_exempt
def view_team_explan(request):
    req = json.loads(request.body)
    year =int(req['year'])
    month = int(req['month'])
    day = int(req['day'])
    meeting_pk = req['meetingPK']
    meetingObj = Meeting.objects.all().get(id=meeting_pk)
    username = request.user.username

    today = date(year,month,day)

    # if meeting_name == '':
    plans= PublicPlan.objects.all().filter(meetings = meetingObj, startTime__lte = today + timedelta(days=1), endTime__gte = today)
    # else:
    
    #     meetingObj = Meeting.objects.all().filter(owner = request.user).get(meeting_name = meeting_name)
    #     plans = Plan.objects.all().filter(meeting = meetingObj, startTime__month = month, startTime__year = year)
    
    plans = serializers.serialize('json', plans)

    if request.user.image == "":
        return JsonResponse({'plans': plans, 'today': day,'userimg':request.user.default_image})
    else:
        return JsonResponse({'plans': plans,'today': day,'userimg':request.user.image.url})

  

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

def meeting_info(request, pk, *args, **kwargs):
    meeting = Meeting.objects.get(id=pk)
    users = meeting.users.all()
    context = {
        'meeting': meeting,
        'users': users,
    }
    return render(request, 'meeting_info.html', context=context)

def generate_invitation_code(length=10):
    return base64.urlsafe_b64encode(
        codecs.encode(uuid.uuid4().bytes, "base64").rstrip()
    ).decode()[:length]
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http.request import HttpRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PrivatePlan ,PublicPlan, Comment, Meeting, Share, PrivateComment, PublicComment, replyPrivateComment, replyPublicComment, Profile
import json
from django.core import serializers
from datetime import date, timedelta, datetime
from . import forms
from django.contrib import auth
from .validators import *
from django.core import serializers
from django.forms.models import model_to_dict
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from itertools import chain
from django.urls import reverse
import random
import uuid
import base64
import codecs
from datetime import datetime
from django.contrib import messages
# main 페이지 접속 시 실행 함수
# 디폴트 달력은 개인 달력
# 모임 생성 유저는 자동으로 users에 들어감
@csrf_exempt
def main(request:HttpRequest,*args, **kwargs):
  login_user = request.user
  meetings = login_user.user_meetings.all()
  try:
    viewDate = request.GET['select-date'].split('-')
    year = viewDate[0]
    month = viewDate[1]
    login_user.current_date = f"{year}-{month}-01"
    login_user.save()
  except:
    year = login_user.current_date.year
    month = login_user.current_date.month
  context = {
            'meetings' : meetings,
            'meeting_name': '',
            'view_year': year,
            'view_month': month,
            }

  return render(request, "main.html", context=context)

@csrf_exempt
def meeting_calendar(request, pk, *args, **kwargs):
  login_user = request.user
  # Review : login_user가 없으면 에러 발생. 핸들링 필요
  # Review : 혹은 @login_required 데코레이터 필요
  cur_meeting = get_object_or_404(Meeting, id=pk)
#   cur_meeting = Meeting.objects.all().get(id=pk)

  meetings = login_user.user_meetings.all()
  try:
    viewDate = request.GET['select-date'].split('-')
    year = viewDate[0]
    month = viewDate[1]
    login_user.current_date = f"{year}-{month}-01"
    login_user.save()
  except:
        year = login_user.current_date.year
        month = login_user.current_date.month
  context = {'cur_meeting': cur_meeting,
             'meetings': meetings,
             'view_year': year,
            'view_month': month,
            }
  return render(request, "meeting_main.html", context=context)


# 미팅 pt 입니다--------------------------------------------------------------
@csrf_exempt
def meeting_create(request:HttpRequest, *args, **kwargs):
    if request.method == 'POST':
        default_image_index = random.randint(1, 10)
        # Review : 변수명 CamelCase vs snake_head 통일 필요
        meeting_name = request.POST.get("meeting_name", '')
        content = request.POST.get("content")
        category = request.POST.get("category")
        if meeting_name == '' or category == '==카테고리 선택==':
          err_msg="모임 이름과 카테고리를 입력하세요"
          context = {
            "meeting_name": meeting_name,
            "content": content,
            "category": category,
            "category_list": Meeting.MEETING_CHOICE,
            'err_msg':err_msg,
          }
          return render(request, "meeting_create.html", context=context)
        else:
          newMeeting = Meeting.objects.create(
          meeting_name = meeting_name,
          content = content,
          owner = request.user,
          category = category,
          invitation_code = generate_invitation_code(),
          image = request.FILES.get("image"),
          default_image = f'/static/default_image/t{default_image_index}.png',
          )
          newMeeting.users.add(request.user)
          return redirect('wapl:meeting_calendar', newMeeting.id)
    category_list = Meeting.MEETING_CHOICE
    context = {
        "category_list":category_list
    }

    return render(request, "meeting_create.html", context=context)

def meeting_detail(request:HttpRequest, pk, *args, **kwargs):
    meeting = get_object_or_404(Meeting, id=pk)
    # meeting = Meeting.objects.get(id=pk)
    context = {
        "meeting" : meeting
    }
    return render(request, "test_meeting_detail.html", context=context)

def meeting_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        meeting = get_object_or_404(Meeting, id=pk)
        # meeting = Meeting.objects.get(id=pk)
        meeting.delete()
        return redirect('wapl:main')

def meeting_join(request:HttpRequest, *args, **kwargs):
    if request.method == "POST":
      code = request.POST["code"]
      try:
          meeting = Meeting.objects.get(invitation_code=code)
          meeting.users.add(request.user)
          return redirect('wapl:meeting_calendar', meeting.id)
      except:
        err_msg = '초대 코드가 다릅니다.'
        context = {'err_msg': err_msg}
        return render(request, 'meeting_join.html', context=context)
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
    title = req['title']
    location = req['location']
    startTime = req['startTime']
    endTime = req['endTime']
    content = req['content']
    shareMeetings = req['shareMeetings']

    login_user = request.user
    meetings = login_user.user_meetings.all()

    result, err_msg = validate_plan(startTime = startTime, endTime = endTime, title = req['title'])
    
    if result:  # validation 통과한 경우
      new_plan = PrivatePlan.objects.create(owner = request.user, startTime = startTime, endTime = endTime, location = location, title = title, content = content)
       # 새로운 share 모델 생성
      for shareMeeting in shareMeetings:
        Share.objects.create(plan=new_plan, meeting=meetings.get(meeting_name=shareMeeting), is_share=shareMeetings[shareMeeting])

      if request.user.profile.image == "":
        userimg = request.user.default_image
      else:
        userimg = request.user.profile.image.url

      new_plan=model_to_dict(new_plan)

      return JsonResponse({'plan':new_plan, 'userimg':userimg, 'err_msg': err_msg})
    else:
      return JsonResponse({'plan': None, 'userimg': None, 'err_msg': err_msg})


@csrf_exempt
def create_public_plan(request, *args, **kwargs):
  if request.method == 'POST':
    req = json.loads(request.body)
    title = req['title']
    location = req['location']
    startTime = req['startTime']
    endTime = req['endTime']
    content = req['content']
    meeting_name = req['meeting_name']

    # meeting = Meeting.objects.get(meeting_name=meeting_name)
    meeting = get_object_or_404(Meeting, meeting_name=meeting_name)

    result, err_msg = validate_plan(startTime = startTime, endTime = endTime, title = req['title'])
    if result:
      new_plan = PublicPlan.objects.create(meetings = meeting,  startTime = startTime, endTime = endTime, location = location, title = title, content = content)

      if meeting.image == "":
        meeting_img = meeting.default_image
      else:
        meeting_img = meeting.image.url

      new_plan=model_to_dict(new_plan)

      return JsonResponse({'plan': new_plan, 'meeting_img': meeting_img, 'err_msg' : err_msg})
    else:
      return JsonResponse({'plan': None, 'meeting_img': None, 'err_msg' : err_msg})

# 개인 일정 수정 함수
# POST로 넘어온 데이터로 updatedPlan 모델 객체 저장
# 리턴하는 값: 에러 메세지 -> 딕셔너리 형태 {key: (Plan 모델 필드)_err, value: (에러 메세지)}
# ex) 날짜 에러인 경우 -> err_msg['time_err'] == "종료 시간이 시작 시간보다 이전일 수 없습니다.
def update(request:HttpRequest, pk, *args, **kwargs):
  plan = get_object_or_404(PrivatePlan, id=pk)
  plan_sT = plan.startTime.strftime('%Y-%m-%d %H:%M:%S')
  plan_eT = plan.endTime.strftime('%Y-%m-%d %H:%M:%S')

  if request.method == "POST":
    plan.startTime = request.POST["startTime"]
    plan.endTime = request.POST["endTime"]
    plan.location = request.POST["location"]
    plan.title = request.POST["title"]
    plan.content = request.POST["content"]
    new_share_list = request.POST.getlist('share-meeting-list[]')
    share_list = list(Share.objects.filter(plan = plan))
    for share in share_list:
      if share.meeting.meeting_name in new_share_list:
        share.is_share = True
        share.save()
      else:
        share.is_share = False
        share.save()     
                    
    plan.save()
    
    return redirect('wapl:detail', pk) 
  
  share_list = list(Share.objects.filter(plan = plan))
  context = {
    'plan': plan,
    'plan_sT': plan_sT,
    'plan_eT': plan_eT,
    'share_list': share_list,
  }
  return render(request, "plan_priUpdate.html", context = context)

# 모임 일정 수정 함수
def pub_update(request:HttpRequest, pk, *args, **kwargs):
    # plan = PublicPlan.objects.get(id=pk)
    plan = get_object_or_404(PublicPlan, id=pk)
    plan_sT = plan.startTime.strftime('%Y-%m-%d %H:%M:%S')
    plan_eT = plan.endTime.strftime('%Y-%m-%d %H:%M:%S')
    
    if request.method == "POST":
        plan.startTime = request.POST["startTime"]
        plan.endTime = request.POST["endTime"]
        plan.location = request.POST["location"]
        plan.title = request.POST["title"]
        plan.content = request.POST["content"]
        plan.save()
        
        return redirect('wapl:pubdetail', pk) 
    return render(request, "plan_pubUpdate.html", {"plan":plan, "plan_sT":plan_sT, "plan_eT":plan_eT})

#개인 일정 삭제 함수
#POST로 넘어온 id값으로 객체 삭제
@csrf_exempt
def delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST":
        plan = get_object_or_404(PrivatePlan, id=pk)
        if plan.owner == request.user:
          plan.delete()
        else:
          err_msg = '본인의 일정만 삭제할 수 있습니다.'
          messages.warning(request, err_msg)
    return redirect('wapl:main')

#모임 일정 삭제 함수
@csrf_exempt
def pub_delete(request:HttpRequest, pk, *args, **kwargs):
    if request.method == "POST": 
        plan = get_object_or_404(PublicPlan, id=pk)
        if plan.owner == request.user or plan.meetings.owner == request.user:
          plan.delete()
        else:
          err_msg = '본인의 일정만 삭제할 수 있습니다.'
          messages.warning(request, err_msg)
          
    return redirect( 'wapl:meeting_calendar',plan.meetings.pk)

#개인 일정 상세보기 함수 + 댓글 생성/리스트 출력까지
def detail(request, pk, *args, **kwargs):
    plan = get_object_or_404(PrivatePlan, pk=pk)
    
    err_msg = ''
    if request.user.is_authenticated:
      if request.method == "POST":
        comments = request.POST["content"]
        result, err_msg = validate_comment(comments)
        if result:            
          PrivateComment.objects.create(
            content=comments,
            user=request.user,
            plan_post=plan,
          )         
          return redirect('wapl:detail', pk) 
        else:
          messages.warning(request, err_msg)
          return redirect('wapl:detail', pk) 
    
    comments = PrivateComment.objects.all().filter(plan_post=plan)
    replys = replyPrivateComment.objects.all()
    context = {
        "plan": plan,
        "comments": comments,
        "replys": replys,
        "err_msg": err_msg,
    }
    return render(request, 'plan_priDetail.html', context=context)

#모임 일정 상세보기 함수 + 댓글 생성/리스트 출력까지
def public_detail(request, pk, *args, **kwargs):
    plan = get_object_or_404(PublicPlan, pk=pk)
    err_msg = ''
    if request.user.is_authenticated:
      if request.method == "POST":
        comments = request.POST["content"]
        result, err_msg = validate_comment(comments)
        if result:
          PublicComment.objects.create(
            content=request.POST["content"],
            user=request.user,
            plan_post=plan,
          )
          return redirect('wapl:pubdetail', pk)
        else:
          messages.warning(request, err_msg)
          return redirect('wapl:pubdetail', pk)
    
    comments = PublicComment.objects.all().filter(plan_post=plan)
    replys = replyPublicComment.objects.all()
    context = {
        "plan": plan,
        "comments" : comments,
        "replys": replys,
        'meeting_pk': plan.meetings.id,
        "err_msg": err_msg,
        }
    return render(request, 'plan_pubDetail.html', context=context)

# 개인 댓글 수정
def comment_update(request, *args, **kwargs):
  pass

# 모임 댓글 수정
def pub_comment_update(request, *args, **kwargs):
  pass

# 개인 대댓글 수정
def reply_update(request, *args, **kwargs):
  pass

# 모임 대댓글 수정
def pub_reply_update(request, *args, **kwargs):
  pass

#개인 일정 대댓글 생성
def reply_create(request, pk, ck, *args, **kwargs):
  comment_post = get_object_or_404(PrivateComment, id=ck)
  if request.user.is_authenticated:
    if request.method == "POST":
      comments = request.POST["content"]
      result, err_msg = validate_comment(comments)
      if result:
        replyPrivateComment.objects.create(
          content=request.POST["content"],
          user=request.user,
          comment_post= comment_post,
        )
        return redirect('wapl:detail', pk)
      else:
        messages.warning(request, err_msg)
        return redirect('wapl:detail', pk)
      
  return redirect('wapl:detail', pk)

#모임 일정 대댓글 생성
def pub_reply_create(request, pk, ck, *args, **kwargs):
    comment_post = get_object_or_404(PublicComment, id=ck)
    if request.user.is_authenticated:
      if request.method == "POST":
        comments = request.POST["content"]
        result, err_msg = validate_comment(comments)
        if result:
          replyPublicComment.objects.create(
              content=request.POST["content"],
              user=request.user,
              comment_post= comment_post,
          )
        else:
          messages.warning(request, err_msg)
          return redirect('wapl:detail', pk)
        
    return redirect('wapl:pubdetail', pk)

#개인 일정 대댓글 삭제
# 댓글 작성자 혹은 해당 일정 작성자는 댓글 삭제 가능
def reply_delete(request:HttpRequest, pk, ck, *args, **kwargs):
    if request.method == "POST": 
      comment = get_object_or_404(replyPrivateComment, id=ck)
      if comment.user == request.user or comment.comment_post.plan_post.owner == request.user:
        comment.delete()
      else:
        err_msg = '댓글을 삭제할 수 없습니다.'
        messages.warning(request, err_msg)
        return redirect('wapl:detail', pk)
    return redirect('wapl:detail', pk)

# 모임 일정 대댓글 삭제
# 댓글 작성자 혹은 해당 모임 소유자는 댓글 삭제 가능
def pub_reply_delete(request:HttpRequest, pk, ck, *args, **kwargs):
    if request.method == "POST":
        comment = get_object_or_404(replyPublicComment, id=ck)
        meeting_owner = comment.comment_post.plan_post.meetings.owner
        if comment.user == request.user or meeting_owner == request.user:
          comment.delete()
        else:
          err_msg = '댓글을 삭제할 수 없습니다.'
          messages.warning(request, err_msg)
          return redirect('wapl:detail', pk)
        
    return redirect('wapl:pubdetail', pk)

# 개인 댓글 삭제
# 댓글 작성자 혹은 해당 개인 일정 작성자는 댓글 삭제 가능
def comment_delete(request:HttpRequest, pk, ak, *args, **kwargs):
    # Review : pk만 있으면 누구나 삭제 가능한데, 의도한 바가 맞나요?
    if request.method == "POST":
      comment = get_object_or_404(PrivateComment, id=pk)
      if comment.user == request.user or comment.plan_post.owner == request.user: 
        comment.delete()
      else:
        err_msg = '댓글을 삭제할 수 없습니다.'
        messages.warning(request, err_msg)
        return redirect('wapl:detail', pk)
      
    return redirect('wapl:detail', ak)

# 모임 댓글 삭제
# 댓글 작성자 혹은 해당 모임 소유자는 댓글 삭제 가능
def pub_comment_delete(request:HttpRequest, pk, ak, *args, **kwargs):
    if request.method == "POST":
      comment = get_object_or_404(PublicComment, id=pk)      
      meeting_owner = comment.plan_post.meetings.owner
      if comment.user == request.user or meeting_owner == request.user:
        comment.delete()
      else:
        err_msg = '댓글을 삭제할 수 없습니다.'
        messages.warning(request, err_msg)
        return redirect('wapl:detail', pk)
      
    return redirect('wapl:pubdetail', ak)

# -------------------------------------------------------------------------
def start(request:HttpRequest, *args, **kwargs):
    return render(request, "test_start.html")

@csrf_exempt
def signup(request:HttpRequest, *args, **kwargs):
    default_image_index = random.randint(1, 4)
    if request.method == 'POST':
        form = forms.SignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            image = request.FILES.get("image")
            profile = Profile(user=user, image=image)
            profile.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('wapl:main')
        else:
            # 오류 메세지 띄워야 함
            # messages.info(request, 'invalid registration details')
            context = {
                'default_src': f'/static/default_image/{default_image_index}.png',
                "form": form,
            }
            return render(request, "signup.html", context=context)
    else:
        context = {
            'default_src': f'/static/default_image/{default_image_index}.png'
        }
        return render(request, template_name='signup.html', context=context)

@csrf_exempt
def extra_signup(request:HttpRequest, *args, **kwargs):
    default_image_index = random.randint(1, 4)
    if request.method == 'POST':
        form = forms.SocialSignupForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            form.save()
            image = request.FILES.get("image")
            profile = Profile(user=request.user, image=image)
            profile.save()
            return redirect('wapl:main')
        else:
            # 정보 틀렸다는 에러 메세지 띄워야 함.
            context = {
                'default_src': f'/static/default_image/{default_image_index}.png',
                "form": form,
            }
            return render(request, "extra_signup.html", context=context)
    else:
        context = {
            'default_src': f'/static/default_image/{default_image_index}.png'
        }
    return render(request, 'extra_signup.html', context=context)

@csrf_exempt
def login(request:HttpRequest, *args, **kwargs):

  if request.method == 'POST':

    form = forms.LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('wapl:main')
    else:
      err_msg="잘못된 ID 또는 패스워드입니다"
      context={
        'err_msg':err_msg
      }
      return render(request, template_name='login.html',context=context)
  else:
        return render(request, template_name='login.html')



def logout(request:HttpRequest, *args, **kwargs):
    login_user = request.user
    login_user.current_date = f'{datetime.now().year}-{datetime.now().month}-01'
    login_user.save()
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

# 개인달력 출력
@csrf_exempt
def view_plan(request):
  req = json.loads(request.body)
  login_user = request.user
  year = login_user.current_date.year
  month = login_user.current_date.month


  private_plans = PrivatePlan.objects.filter(owner=login_user, startTime__year__lte=year, endTime__year__gte=year)

  private_plans = list(private_plans)

  meetings = login_user.user_meetings.all()

  meeting_list = serializers.serialize('json', meetings)
  public_plans = []

  meeting_img = {}

  for i in range(len(meetings)) :
     if meetings[i].image == "":
        meeting_img[meetings[i].pk] = meetings[i].default_image
     else:
        meeting_img[meetings[i].pk] = meetings[i].image.url

  if request.user.profile.image == "":
       userimg = request.user.default_image
  else:
       userimg = request.user.profile.image.url

  for meeting in meetings :
      public_plan = PublicPlan.objects.all().filter(meetings = meeting,startTime__year__lte=year, endTime__year__gte=year)
      public_plans += list(public_plan)

  private_plans = serializers.serialize('json', private_plans)
  public_plans = serializers.serialize('json', public_plans)
  # PrivatePlan에서 owner가 로그인 유저인 Plan 필터링 예정



  return JsonResponse({'public_plans': public_plans,
                         'private_plans':private_plans,'userimg':userimg,
                         'meetingimg':meeting_img,
                         'meetingList': meeting_list})


@csrf_exempt
def view_team_plan(request):
  req = json.loads(request.body)
  login_user = request.user
  year = login_user.current_date.year
  month = login_user.current_date.month
  meeting_pk = req['meetingPK'] 
  # 화면에서 유저가 선택한 모임 pk를 넘겨야 함

  meeting = Meeting.objects.get(id=meeting_pk)
  share_list = list(Share.objects.filter(meeting=meeting, is_share="open"))

  share_list += list(Share.objects.filter(meeting=meeting, is_share="untitled"))

  private_plans = []
  public_plans= []

  for i in range(len(share_list)):
     if share_list[i].plan.startTime.year == share_list[i].plan.endTime.year:
        if share_list[i].plan.startTime.month <= share_list[i].plan.endTime.month:
           private_plans.append(share_list[i].plan)
     else:
        private_plans.append(share_list[i].plan)


  public_plans = list(PublicPlan.objects.all().filter(meetings=meeting, startTime__year__lte=year, endTime__year__gte=year))  

  private_plans = serializers.serialize('json', private_plans)
  public_plans = serializers.serialize('json', public_plans)

  users = meeting.users.all()
  
  user_img = {}
  for i in range(len(users)):
     if users[i].profile.image=="":
        user_img[users[i].pk] = users[i].default_image
     else:
        user_img[users[i].pk] = users[i].profile.image.url

  if meeting.image == "":
     meeting_img = meeting.default_image
  else:
     meeting_img = meeting.image.url

  return JsonResponse({'public_plans': public_plans,
                        'private_plans':private_plans,
                        'user_img':user_img,
                        'meeting_img':meeting_img})

# 날짜 클릭 시 호출 함수
# 해당 날짜에 해당하는 일정들 정보를 넘겨줌
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

  public_plans = []

  if request.user.profile.image == "":
       userimg = request.user.default_image
  else:
       userimg = request.user.profile.image.url

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


  return JsonResponse({'public_plans': public_plans,
                         'private_plans':private_plans,'today': day,'userimg':userimg,
                         'meetingimg':meeting_img})

def list_to_queryset(model, data):
    from django.db.models.base import ModelBase

    if not isinstance(model, ModelBase):
        raise ValueError(
            "%s must be Model" % model
        )
    if not isinstance(data, list):
        raise ValueError(
            "%s must be List Object" % data
        )

    pk_list = [obj.pk for obj in data]
    return model.objects.filter(pk__in=pk_list)

@csrf_exempt
def view_team_explan(request):
    req = json.loads(request.body)
    year =int(req['year'])
    month = int(req['month'])
    day = int(req['day'])
    meeting_pk = req['meetingPK']
    # meeting = Meeting.objects.get(id=meeting_pk)
    meeting = get_object_or_404(Meeting, id=meeting_pk)
    today = date(year,month,day)

    public_plans= PublicPlan.objects.filter(meetings = meeting, startTime__lte = today + timedelta(days=1), endTime__gte = today)

    share_list = list(Share.objects.filter(meeting=meeting, is_share="open"))

    share_list += list(Share.objects.filter(meeting=meeting, is_share="untitled"))

    share_plans = [share.plan for share in share_list]
    share_plans = list_to_queryset(PrivatePlan, share_plans)

    share_plans = list(share_plans.filter(startTime__lte = today + timedelta(days=1), endTime__gte = today))

    users = meeting.users.all()
    
    public_plans = serializers.serialize('json', public_plans)
    private_plans = serializers.serialize('json', share_plans)
    share_list = serializers.serialize('json', share_list)

    user_name = {}

    for i in range(len(users)):
        user_name[users[i].pk] = users[i].nickname

    user_img = {}

    for i in range(len(users)):
      if users[i].profile.image=="":
        user_img[users[i].pk] = users[i].default_image
      else:
        user_img[users[i].pk] = users[i].profile.image.url

    if meeting.image == "":
      meeting_img = meeting.default_image
    else:
      meeting_img = meeting.image.url

    return JsonResponse({'public_plans': public_plans,
                         'private_plans':private_plans,
                         'share_list' : share_list,
                         'user_name' : user_name,
                         'user_img':user_img,
                         'meeting_img':meeting_img})

# 프로필 업데이트 함수
def profile(request:HttpRequest, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("wapl:login")

    if request.method == "POST":
        form = forms.EditProfileForm(request.POST or None, request.FILES or None, instance=request.user)
        if form.is_valid():
            form.save()
            profile = request.user.profile
            image = request.FILES.get('image')
            check = request.POST.getlist('image-clear')
            if image or len(check) > 0:
                profile.image = image
                profile.save()
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
    # Review : pk만 있으면 누구나 미팅을 볼 수 있는데, 의도한 바가 맞나요?
    # meeting = Meeting.objects.get(id=pk)
    meeting = get_object_or_404(Meeting, id=pk)
    users = meeting.users.all()
    context = {
        'meeting': meeting,
        'users': users,
    }
    return render(request, 'meeting_info.html', context=context)

def meeting_info_edit(request, pk, *args, **kwargs):
    # Review : pk만 있으면 누구나 미팅을 수정할 수 있는데, 의도한 바가 맞나요?
    # meeting = Meeting.objects.get(id=pk)
    meeting = get_object_or_404(Meeting, id=pk)

    if request.method == "POST":
        meeting.meeting_name = request.POST["meeting_name"]
        meeting.category = request.POST["category"]
        meeting.content = request.POST["content"]
        default_check = request.POST.getlist("image-clear")
        if len(default_check) == 0:
            meeting.image = request.FILES.get("image")
        else:
            meeting.image.delete()
        meeting.save()

        return redirect('wapl:meeting_info', pk)

    users = meeting.users.all()
    category_list = Meeting.MEETING_CHOICE
    context = {
        'meeting': meeting,
        'users': users,
        'category_list': category_list,
    }
    return render(request, 'meeting_info_edit.html', context=context)

def generate_invitation_code(length=10):
    return base64.urlsafe_b64encode(
        codecs.encode(uuid.uuid4().bytes, "base64").rstrip()
    ).decode()[:length]

def select_date_main(request, *args, **kwargs):
    req = json.loads(request.body)
    year = req['year']
    month = req['month']
    login_user = request.user
    login_user.current_date = f"{year}-{month}-01"
    login_user.save()

    return redirect('wapl:main')

def select_date_meeting(request, *args, **kwargs):
    req = json.loads(request.body)
    year = req['year']
    month = req['month']
    meeting_id = req['meeting_id']
    login_user = request.user
    login_user.current_date = f"{year}-{month}-01"
    login_user.save()

    return redirect('wapl:meeting_calendar', meeting_id)


# -----------------에러 페이지 설정---------------------
# handler400 = 'wapl.views.bad_request_page'
def bad_request_page(request, exception):
    return render(request, 'error_page/error_400.html')

# handler403 = 'wapl.views.permission_denied_page'
def permission_denied_page(request, exception):
    return render(request, 'error_page/error_403.html')

# handler404 = 'wapl.views.page_not_found_page'
def page_not_found_page(request, exception):
    return render(request, 'error_page/error_404.html')

# handler500 = 'wapl.views.server_error_page'
def server_error_page(request):
    return render(request, 'error_page/error_500.html')
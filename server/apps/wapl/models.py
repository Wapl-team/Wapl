from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.validators import MinLengthValidator

# 유저
# 필드: 본명, 닉네임, 이메일, 이미지
class User(AbstractUser):
  first_name = None
  last_name = None
  name = models.CharField(max_length=20)
  nickname = models.CharField(max_length=20)
  # Review : None인 이유가 있나요?
  birth = None
  gender = None
  job = None
  desc = None
  email = models.EmailField(null=True)
  image = models.ImageField(blank=True, upload_to='profile')
  default_image = models.CharField(null=True, max_length=200)
  current_date = models.DateField(auto_now_add=True, null=True)

# 일정
# 필드: 시작시간, 끝시간, 제목, 장소, 내용, 작성자(owner)
class Plan(models.Model):
  startTime = models.DateTimeField()
  endTime = models.DateTimeField()
  location = models.CharField(max_length=20, blank=True)
  title = models.CharField(max_length=20)
  content = models.TextField(blank=True)

  class Meta:
    abstract = True
  def __str__(self):
    return self.title

# 모임
# 필드: 카테고리, 모임 이름, 내용, 모임 소융 유저
class Meeting(models.Model):

    MEETING_CHOICE = [
        ('family', '가족'),
        ('couple', '연인'),
        ('club', '동아리'),
        ('friend', '친구'),
        ('school', '학교'),
        ('company', '회사'),
    ]

    meeting_name = models.CharField(max_length=20)
    content = models.TextField()
    category = models.CharField(choices=MEETING_CHOICE, max_length=20)
    owner = models.ForeignKey(User, related_name="meetings", on_delete=models.DO_NOTHING, default=1)
    users = models.ManyToManyField(User, related_name="user_meetings")
    invitation_code = models.CharField(max_length=20, null=True)
    image = models.ImageField(blank=True, upload_to='team_profile')
    default_image = models.CharField(null=True, max_length=200)

    def __str__(self):
        return self.meeting_name

class PrivatePlan(Plan):
  owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plans', default=1)

class PublicPlan(Plan):
  meetings = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='plans', default=1)

class Share(models.Model):
  plan = models.ForeignKey(PrivatePlan, on_delete=models.CASCADE, related_name='plan_shares', default=1)
  meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='meeting_shares', default=1)
  is_share = models.BooleanField()

# 댓글
# 필드: 내용, 생성시간, 작성 유저, 일정
class Comment(models.Model):
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    @property
    def created_string(self):
        time = timezone.now() - self.created_at

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분 전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간 전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created_at.date()
            return str(time.days) + '일 전'
        else:
            return False
    
    class Meta:
      abstract = True


class PrivateComment(Comment):
  plan_post=models.ForeignKey(PrivatePlan, on_delete=models.CASCADE)
  
class replyPrivateComment(Comment):
  comment_post=models.ForeignKey(PrivateComment, on_delete=models.CASCADE)
  
class PublicComment(Comment):
  plan_post=models.ForeignKey(PublicPlan, on_delete=models.CASCADE)
  
class replyPublicComment(Comment):
  comment_post=models.ForeignKey(PublicComment, on_delete=models.CASCADE)
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
    birth = None
    gender = None
    job = None
    desc = None
    email = models.EmailField(null=True)
    image = models.ImageField(blank=True, upload_to='profile')
    default_image = models.CharField(null=True, max_length=200)

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
    owner = models.ForeignKey(User, related_name="meeting", on_delete=models.CASCADE, default=1)
    users = models.ManyToManyField(User, related_name="meeting_user", symmetrical=False)
    
    def __str__(self):
        return self.meeting_name
    
    
# 일정
# 필드: 시작시간, 끝시간, 제목, 장소, 내용, 작성자(User)
class Plan(models.Model):
  startTime = models.DateTimeField()
  endTime = models.DateTimeField()
  location = models.CharField(max_length=20, blank=True)
  title = models.CharField(max_length=20)
  content = models.TextField(blank=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_plan', default=1)
  meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='meeting_plan', blank=True, null=True)
  
  def __str__(self):
    return self.title


# 댓글
# 필드: 내용, 생성시간, 작성 유저, 일정
class Comment(models.Model):
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    plan_post=models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="comment_post") 
    
    @property
    def created_string(self):
        time = datetime.now(tz=timezone.utc) - self.created_at

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



from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
from django.utils import timezone


class Comment(models.Model):
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.TextField(default='')
    plan_post = models.TextField(default='')

    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    # plan_post=models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="comment_post") 
    
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

#멤버 변수: 시작시간, 끝시간, 제목, 장소, 내용, 작성자(User)
class Plan(models.Model):
  startTime = models.DateTimeField(null=False)
  endTime = models.DateTimeField(null=False)
  location = models.CharField(max_length=20, null=False, blank=True)
  title = models.CharField(max_length=20, null=False)
  content = models.TextField(blank=True)
  # user = models.ForeignKey(User)
  
  def __str__(self):
    return self.title
  

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


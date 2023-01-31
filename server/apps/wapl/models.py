from django.db import models
from django.contrib.auth.models import AbstractUser

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
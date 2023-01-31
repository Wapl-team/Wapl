from django.db import models
from django.contrib.auth.models import AbstractUser

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
    kakao_id = models.IntegerField(default=-1)
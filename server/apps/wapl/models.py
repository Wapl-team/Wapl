from django.db import models

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
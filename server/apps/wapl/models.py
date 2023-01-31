from django.db import models
from datetime import datetime, timedelta

class Comment(models.Model):
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.TextField(default='')
    plan_post = models.TextField(default='')

    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_user")
    # plan_post=models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="comment_post") 
    
from django.contrib import admin
from . import models

  

admin.site.register(models.PublicPlan)
admin.site.register(models.PrivatePlan)
admin.site.register(models.User)
admin.site.register(models.Meeting)
admin.site.register(models.Share)
admin.site.register(models.PrivateComment)
admin.site.register(models.PublicComment)
admin.site.register(models.replyPublicComment)
admin.site.register(models.replyPrivateComment)
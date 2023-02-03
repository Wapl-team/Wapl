from django.contrib import admin
from . import models

  
admin.site.register(models.Comment)
admin.site.register(models.PublicPlan)
admin.site.register(models.PrivatePlan)
admin.site.register(models.User)
admin.site.register(models.Meeting)
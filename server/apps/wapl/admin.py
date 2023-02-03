from django.contrib import admin
from . import models

class PublicPlanAdmin(admin.ModelAdmin):
  model = models.PublicPlan
  list_display = ['title', 'owner', 'get_meetings']
  @admin.display(ordering='meeting__plans', description='Meeting')
  def get_meetings(self, obj):
    return obj.plan_meetings.all()
  
  
admin.site.register(models.Comment)
admin.site.register(models.PublicPlan, PublicPlanAdmin)
admin.site.register(models.User)
admin.site.register(models.Meeting)
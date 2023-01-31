from django.contrib import admin
from . import models
admin.site.register(models.Comment)
admin.site.register(models.Plan)
admin.site.register(models.User)
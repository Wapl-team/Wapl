from django.urls import path
from . import views

app_name = "wapl"

urlpatterns= [
    path("", views.main, name="main"),
    path("create", views.create, name="create"), # 용현님 일정 ajax
    path("update", views.update, name="update"), # 용현님 일정 ajax
    path("retrieve", views.retrieve, name="retrieve"), # 용현님 일정 ajax
    path("delete", views.delete, name="delete"), # 용현님 일정 ajax
    path('plan/<int:pk>', views.detail, name='detail')
]
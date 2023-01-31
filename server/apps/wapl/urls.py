from django.urls import path
from . import views

app_name = "wapl"

urlpatterns= [
    path("", views.main, name="main"),
]
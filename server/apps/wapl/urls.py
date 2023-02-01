from django.urls import path
from . import views

app_name = "wapl"

urlpatterns= [
    path("main", views.main, name="main"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("", views.start, name="start"),
    path("create", views.create, name="create"), 
    path("update", views.update, name="update"), 
    path("retrieve", views.retrieve, name="retrieve"), 
    path("delete", views.delete, name="delete"), 
    path('plan/<int:pk>', views.detail, name='detail'),
    path("comment/", views.comment, name="comment"),
    path("comment/<int:pk>/delete", views.comment_delete, name="comment_delete"),
    path('view_plan/', views.view_plan, name='view_plan'),
]


from django.urls import path
from . import views

app_name = "wapl"

# urlpatterns= [
#     path("", views.main, name="main"),
#     path("login", views.login, name="login"),
#     path("logout", views.logout, name="logout"),
#     path("signup", views.signup, name="signup"),
#     path("plan", views.create, name="create"), # 용현님 일정 ajax
#     path("plan/<int:pk>", views.comment, name="comment"), # 윤정님 일정 상세
# ]


urlpatterns = [
    path("comment/", views.comment, name="comment"),
    path("comment/<int:pk>/delete", views.comment_delete, name="comment_delete"),
]

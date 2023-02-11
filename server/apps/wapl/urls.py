from django.urls import path
from . import views

app_name = "wapl"

urlpatterns= [
    # Review : Restful한 CRUD 패턴을 준수하는 게 좋습니다!
    path("main", views.main, name="main"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("signup", views.signup, name="signup"),
    path("", views.start, name="start"),
    path("create-private-plan", views.create_private_plan, name="create_private_plan"), 
    path("create-public-plan", views.create_public_plan, name="create_public_plan"), 
    path('view_plan/', views.view_plan, name='view_plan'),
    path('view_explan/', views.view_explan, name='view_explan'),
    path('view_team_plan/', views.view_team_plan, name='view_team_plan'),
    path('view_team_explan/', views.view_team_explan, name='view_team_explan'),
    
# 개인 일정 관련
    path("plan/<int:pk>/update", views.update, name="update"), 
    path("plan/<int:pk>/delete", views.delete, name="delete"), 
    path('plan/<int:pk>', views.detail, name='detail'),
    path("plan/<int:ak>/<int:pk>/delete", views.comment_delete, name="comment_delete"),
    path("plan/<int:pk>/comment/<int:ck>", views.reply_create, name="reply_create"),
    path("plan/<int:pk>/comment/<int:ck>/delete", views.reply_delete, name="reply_delete"),
    
# 모임 일정 관련
    path("pubplan/<int:pk>/update", views.pub_update, name="pubupdate"), 
    path("pubplan/<int:pk>/delete", views.pub_delete, name="pubdelete"), 
    path('pubplan/<int:pk>', views.public_detail, name='pubdetail'),
    path("pubplan/<int:ak>/<int:pk>/delete", views.pub_comment_delete, name="pubcomment_delete"),
    path("pubplan/<int:pk>/comment/<int:ck>", views.pub_reply_create, name="pubreply_create"),
    path("pubplan/<int:pk>/comment/<int:ck>/delete", views.pub_reply_delete, name="pubreply_delete"),

    path('profile', views.profile, name='profile'),
    path('password/update', views.update_password, name='update_password'),
    path("main/meeting/create", views.meeting_create, name="meeting_create"),
    path("meeting/<int:pk>", views.meeting_calendar, name="meeting_calendar"),
    path("meeting/<int:pk>/delete", views.meeting_delete, name="meeting_delete"),
    path("meeting/info/<int:pk>", views.meeting_info, name="meeting_info"),
    path("meeting/join", views.meeting_join, name="meeting_join"),

    # url(r'', views.)

]

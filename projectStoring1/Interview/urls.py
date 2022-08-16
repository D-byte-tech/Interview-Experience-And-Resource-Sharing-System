from django.contrib import admin
from django.urls import path, include
from Interview import views

urlpatterns = [

    path('', views.welcome, name='welcome'),
    path('userinfo', views.userinfo, name='userinfo'),
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout, name='logout'),
    path('interview', views.interview, name='interview'),
    path('resource', views.resource, name='resource'),
    path('index', views.index, name='index'),
    path('resourcetile', views.resourcetile, name='resourcetile'),
    path('interviewtile', views.interviewtile, name='interviewtile'),
    path('interviewExperiences/<str:cname>', views.interviewExperiences, name='interviewExperiences'),
    path('resources/<str:sname>', views.resources, name='resources'),
    path('interviewExperiences/profiletest/<str:Userid>', views.profiletest, name='profiletest'),
    path('resources/profiletest/<str:Userid>', views.profiletest, name='profiletest'),
    path('updateProfile', views.updateProfile, name='updateProfile'),
    path('profile', views.user_profile, name='user_profile'),
    path('changepwd/<token>', views.change_pwd, name='change_pwd'),
    path('forgetpwd', views.forget_pwd, name='forget_pwd'),
  
]






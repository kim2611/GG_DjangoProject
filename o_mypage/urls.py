from django.contrib import admin
from django.urls import path, include
from bcuser.views import *
from .import views


urlpatterns = [
    path('main/', views.mypage_main, name='mypage_main'),
    path('write/', views.mypage_write, name='mypage_write'),
    path('detail/<int:writer_id>/', views.mypage_detail, name='mypage_detail'),
]
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name="chat_board_list" ),
    path('write/', views.board_write, name="chat_write_list"),
    path('<int:pk>/',views.board_detail, name="chat_board_detail")] 
    

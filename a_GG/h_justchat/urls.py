from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name="chat_board_list" ),   # 127.0.0.1:8000/notice_board/list
    path('write/', views.board_write, name="chat_write_list")]   # 127.0.0.1:8000/notice_board/list
    #path('detail/<int:pk>/', c_BoardDetail.as_view()),]  # 127.0.0.1:8000/notice_board/
    # path('update/<int:pk>/', views.c_Boardupdate, name="board_update"),  # 127.0.0.1:8000/notice_board/update/
    # path('delete/<int:pk>/', views.c_Boarddelete)  # 127.0.0.1:8000/notice_board/delete/
    

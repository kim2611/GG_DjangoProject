from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', c_BoradList.as_view(), name="notice_board_list"),    # 127.0.0.1:8000/notice_board/list
    path('write/', c_board_write),    # 127.0.0.1:8000/notice_board/list
    path('detail/<int:pk>/', c_BoardDetail.as_view()),  # 127.0.0.1:8000/notice_board/
    # path('update/<int:pk>/', views.c_Boardupdate, name="board_update"),  # 127.0.0.1:8000/notice_board/update/
    # path('delete/<int:pk>/', views.c_Boarddelete)  # 127.0.0.1:8000/notice_board/delete/
]

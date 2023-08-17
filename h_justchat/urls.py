from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.board_list, name="chat_board_list" ),
    path('write/', views.board_write, name="chat_write_list"),
    path('<int:pk>/', Board_detail.as_view(), name="chat_board_detail"), 
    path('delete/<int:pk>/',views.board_delete, name="chat_board_delete"),
    path('comment_delete/<int:pk>/',views.comment_delete, name="chat_comment_delete"),
    path('update/<int:pk>/',views.board_update, name="chat_board_update"),
    path('vote/<int:pk>/',views.board_vote, name="chat_board_vote")
    ] 

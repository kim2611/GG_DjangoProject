from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.board_list, name="chat_board_list" ),
    path('write/', views.board_write, name="chat_write_list"),
    path('<int:pk>/', Board_detail.as_view(), name="chat_board_detail"), 
    path('<int:pk>/delete/',views.board_delete, name="chat_board_delete"),
    path('<int:pk>/comment_delete/',views.comment_delete, name="chat_comment_delete"),
    path('<int:pk>/update/',views.board_update, name="chat_board_update"),
    path('<int:pk>/vote/',views.board_vote, name="chat_board_vote")
    ] 

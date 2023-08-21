from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.board_list, name="qna_board_list" ),
    path('write/', views.board_write, name="qna_write_list"),
    path('<int:pk>/', Board_detail.as_view(), name="qna_board_detail"), 
    path('delete/<int:pk>/',views.board_delete, name="qna_board_delete"),
    path('comment_delete/<int:pk>/',views.comment_delete, name="qna_comment_delete"),
    path('update/<int:pk>/',views.board_update, name="qna_board_update"),
    path('vote/<int:pk>/',views.board_vote, name="qna_board_vote")
    ] 

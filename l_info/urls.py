from django.contrib import admin
from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.board_list, name="info_board_list" ),
    path('write/', BoardWriteView.as_view(), name="info_write_list"),
    path('<int:pk>/', Board_detail.as_view(), name="info_board_detail"), 
    path('delete/<int:pk>/', BoardDeleteView.as_view(), name="info_board_delete"),
    path('comment_delete/<int:pk>/',views.comment_delete, name="info_comment_delete"),
    path('update/<int:pk>',BoardUpdateView.as_view(), name="info_board_update"),
    path('vote/<int:pk>/',views.board_vote, name="info_board_vote")
    ] 

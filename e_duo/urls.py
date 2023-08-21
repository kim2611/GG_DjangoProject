from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.board_list, name="duo_board_list" ),
    path('write/', views.board_write, name="duo_write_list"),
    path('<int:pk>/', Board_detail.as_view(), name="duo_board_detail"), 
    path('delete/<int:pk>/',views.board_delete, name="duo_board_delete"),
    path('comment_delete/<int:pk>/',views.comment_delete, name="duo_comment_delete"),
    path('update/<int:pk>/',views.board_update, name="duo_board_update"),
    path('vote/<int:pk>/',views.board_vote, name="duo_board_vote")
    ] 

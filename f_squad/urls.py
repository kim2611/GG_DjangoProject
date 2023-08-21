from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.board_list, name="squad_board_list" ),
    path('write/', views.board_write, name="squad_write_list"),
    path('<int:pk>/', Board_detail.as_view(), name="squad_board_detail"), 
    path('delete/<int:pk>/',views.board_delete, name="squad_board_delete"),
    path('comment_delete/<int:pk>/',views.comment_delete, name="squad_comment_delete"),
    path('update/<int:pk>/',views.board_update, name="squad_board_update"),
    path('vote/<int:pk>/',views.board_vote, name="squad_board_vote")
    ] 

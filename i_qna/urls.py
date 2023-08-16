from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.board_list, name="qna_board_list" ),
    path('write/', views.board_write, name="qna_write_list"),
    path('<int:pk>/', Board_detail.as_view(), name="qna_board_detail"), 
    path('<int:pk>/delete/',views.board_delete, name="qna_board_delete"),
    path('<int:pk>/comment_delete/',views.comment_delete, name="qna_comment_delete"),
    path('<int:pk>/update/',views.board_update, name="qna_board_update"),
    path('<int:pk>/vote/',views.board_vote, name="qna_board_vote")
    ] 
from django.contrib import admin
from django.urls import path, include
from bcuser.views import *
from h_justchat.views import *
#from c_notice.views import *
from k_sellboard.views import (
    ProductList, ProductCreate, ProductDetail)
from . import views



urlpatterns = [
    path('sellboard/',ProductList.as_view(), name='sellboard'),
    path('sellboard/create/', ProductCreate.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view(),name='product_detail'),
    path('<int:pk>/sellupdate/', views.post_update, name='product_update'),
    path('<int:pk>/k_comment_delete/',views.k_comment_delete, name="comment_delete"),
    path('product/<int:pk>/delete/', views.post_delete, name='product_delete'),
    path('vote/<int:pk>/',views.board_vote, name="product_jjim")

]
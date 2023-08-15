from django.contrib import admin
from django.urls import path, include
from bcuser.views import *
from h_justchat.views import *
#from c_notice.views import *
from j_buyboard.views import (
    ProductList, ProductCreate, ProductDetail)
from . import views
# from n_order.views import OrderCreate, OrderList












urlpatterns = [
    path('buyboard/',ProductList.as_view(), name='buyboard'),
    path('buyboard/create/', ProductCreate.as_view()),
    path('product/<int:pk>/', ProductDetail.as_view()),
    # path('order/create/', OrderCreate.as_view()),
    # path('order/', OrderList.as_view()),


    ############## 수성 삭제 시 urls ################
    # path('<int:pk>/', views.j_buy_detail, name="chat_board_detail"), 
    # path('buyboard/<int:pk>/delete/', views.board_delete, name="chat_board_delete"),
    # path('<int:pk>/update/',views.board_update, name="chat_board_update")
    ] 
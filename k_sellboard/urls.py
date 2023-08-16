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
    path('product/<int:pk>/', ProductDetail.as_view()),
]
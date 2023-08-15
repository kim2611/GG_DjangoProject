from django.contrib import admin
from django.urls import path, include
from bcuser.views import *
from h_justchat.views import *
#from c_notice.views import *
from n_order.views import OrderCreate,product_detail
# from n_order.views import OrderList
from . import views







urlpatterns = [    
    # path('order/create/', OrderCreate.as_view()),
    # path('order/', OrderList.as_view()),
    path('order/create/', OrderCreate.as_view(), name='create_order'),
    path('product/<int:pk>/', product_detail, name='product_detail'),
]
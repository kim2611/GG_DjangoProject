from django.contrib import admin
from django.urls import path, include
from bcuser.views import *
from h_justchat.views import *
#from c_notice.views import *
from n_order.views import OrderCreate
from n_order.views import OrderList
from . import views







urlpatterns = [    
    path('order/create/', OrderCreate.as_view()),
    path('order/', OrderList.as_view()),

]
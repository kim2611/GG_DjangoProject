from django.contrib import admin
from django.urls import path, include
from bcuser.views import *
from j_buyboard.views import (
    buyProductList, buyProductCreate, buyProductDetail)
from .import views












urlpatterns = [
    path('buyboard/',buyProductList.as_view(), name='buyboard'),
    path('buyboard/create/', buyProductCreate.as_view()),
    path('buyproduct/<int:pk>/', buyProductDetail.as_view(), name='buyproduct_detail'),
    path('<int:pk>/update/', views.post_update, name='buyproduct_update'),
    path('buyproduct/<int:pk>/delete/', views.post_delete, name='buyproduct_delete'),
    path('<int:pk>/comment_delete/',views.comment_delete, name="comment_delete"),


]

"""
URL configuration for a_GG project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bcuser.views import *
from h_justchat.views import *
#from c_notice.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout),
    path('register/', RegisterView.as_view()),
    
    #path("notice_board/", include('c_notice.urls')), # 127.0.0.1:8000/notice_board/
    path("chat_board/", include('h_justchat.urls')), # 127.0.0.1:8000/notice_board/
    path("", include('k_sellboard.urls')),
    path("", include('n_order.urls')),
    path("qna_board/", include('i_qna.urls')),
]

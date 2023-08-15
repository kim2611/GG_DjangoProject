from django.contrib import admin
from django.urls import path, include
from bcuser.views import *
#from h_justchat.views import *
#from c_notice.views import *
from o_mypage.views import MypageGame, MypageWrite, MypageUpdate

urlpatterns = [    
    path('mypage/', ),
    path('mypage/gamelist/', MypageGame.as_view()),
    path('mypage/writelist/', MypageWrite.as_view()),
    path('mypage/update/', MypageUpdate.as_view()),
    
]
from django.contrib import admin
from .models import Mypage

# class TimeChoiceAdmin(admin.ModelAdmin):
#     list_display = ('time',)  # TimeChoice 객체를 어떻게 표시할지 설정

# admin.site.register(TimeChoice, TimeChoiceAdmin)

class MypageAdmin(admin.ModelAdmin):
    list_display = ('writer','age', 'gender')  # Mypage 객체를 어떻게 표시할지 설정

admin.site.register(Mypage, MypageAdmin)






from django.contrib import admin
from .models import *
# Register your models here.

class c_NoticeAdmin(admin.ModelAdmin) :
    list_display=('c_title', 'c_writer')
    
admin.site.register(c_Notice,c_NoticeAdmin)

class c_CommentAdmin(admin.ModelAdmin) :
    list_display=('post', 'comment')
    
admin.site.register(c_Comment,c_CommentAdmin)
from django.contrib import admin
from .models import i_Qna, i_Comment
# Register your models here.

class I_QnaAdmin(admin.ModelAdmin) :
    list_display=('i_title', 'i_writer')
    
admin.site.register(i_Qna,I_QnaAdmin)

class i_CommentAdmin(admin.ModelAdmin) :
    list_display=('post', 'comment')
    
admin.site.register(i_Comment,i_CommentAdmin)
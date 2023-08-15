from django.contrib import admin
from .models import h_Chat, h_Comment
# Register your models here.

class h_ChatAdmin(admin.ModelAdmin) :
    list_display=('h_title', 'h_writer')
    
admin.site.register(h_Chat,h_ChatAdmin)

class h_CommentAdmin(admin.ModelAdmin) :
    list_display=('post', 'comment')
    
admin.site.register(h_Comment,h_CommentAdmin)
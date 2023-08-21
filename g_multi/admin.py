from django.contrib import admin
from .models import g_Multi,g_Comment

class g_MultiAdmin(admin.ModelAdmin) :
    list_display=('g_title', 'g_writer')
    
admin.site.register(g_Multi,g_MultiAdmin)

class g_CommentAdmin(admin.ModelAdmin) :
    list_display=('post', 'comment')
    
admin.site.register(g_Comment,g_CommentAdmin)
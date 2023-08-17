from django.contrib import admin
from .models import f_Squad, f_Comment

class f_SquadAdmin(admin.ModelAdmin) :
    list_display=('f_title', 'f_writer')
    
admin.site.register(f_Squad,f_SquadAdmin)

class f_CommentAdmin(admin.ModelAdmin) :
    list_display=('post', 'comment')
    
admin.site.register(f_Comment,f_CommentAdmin)
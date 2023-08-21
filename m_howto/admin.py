from django.contrib import admin
from .models import m_Howto, m_Comment

class m_HowtoAdmin(admin.ModelAdmin) :
    list_display=('m_title', 'm_writer')
    
admin.site.register(m_Howto,m_HowtoAdmin)

class m_CommentAdmin(admin.ModelAdmin) :
    list_display=('post', 'comment')
    
admin.site.register(m_Comment,m_CommentAdmin)

# Register your models here.

from django.contrib import admin
from .models import h_Chat
# Register your models here.

class h_ChatAdmin(admin.ModelAdmin) :
    list_display=('h_title', 'h_writer')
    
admin.site.register(h_Chat,h_ChatAdmin)


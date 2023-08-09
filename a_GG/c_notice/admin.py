from django.contrib import admin
from .models import c_Board
# Register your models here.

class c_BoardAdmin(admin.ModelAdmin) :
    list_display=('title', )
    
admin.site.register(c_Board, c_BoardAdmin)
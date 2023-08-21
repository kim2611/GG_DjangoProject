from django.contrib import admin
from .models import buyProduct
# Register your models here.

class j_buyProductAdmin(admin.ModelAdmin) :
    list_display=('name', 'price')
    
admin.site.register(buyProduct,j_buyProductAdmin)


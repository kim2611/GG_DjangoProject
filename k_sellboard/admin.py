from django.contrib import admin
from .models import Product
# Register your models here.

class j_ProductAdmin(admin.ModelAdmin) :
    list_display=('name', 'price')
    
admin.site.register(Product,j_ProductAdmin)


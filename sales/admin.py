from django.contrib import admin
from .models import Product, SalesInfo

class ProductAdmin(admin.ModelAdmin):
    search_fields = ['type', 'pname']

admin.site.register(Product, ProductAdmin)

class SalesInfoAdmin(admin.ModelAdmin):
    search_fields = ['type', 'pname']

admin.site.register(SalesInfo, SalesInfoAdmin)
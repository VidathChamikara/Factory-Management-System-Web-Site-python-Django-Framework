from django.contrib import admin
from .models import Product, Order
from django.contrib.auth.models import Group

# create admin panel name
admin.site.site_header = 'Kaley Tea Inventory Dashboard'


# create admin panel product table


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'leaves_category', 'in_date', 'in_time', 'tray_id', 'temparature', 'tea_weight', 'out_date')
    list_filter = ['leaves_category']


class OrderAdmin(admin.ModelAdmin):
    list_display = ('leaves_category', 'order_quantity', 'staff', 'date', 'time')
    list_filter = ['leaves_category']


# Register your models here.
# admin.site.unregister(Group)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)

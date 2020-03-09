from django.contrib import admin

from sale.models import Order, Order_Products, Type, Product

# Register your models here.
admin.site.register(Order)

admin.site.register(Order_Products)

admin.site.register(Type)

admin.site.register(Product)
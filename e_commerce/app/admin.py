from django.contrib import admin

# Register your models here.
from .models import  Product, Order, CartItem, User
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CartItem)
# admin.site.register(Seller)


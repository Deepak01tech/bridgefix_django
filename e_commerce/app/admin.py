from django.contrib import admin

# Register your models here.
from .models import  Product, Order, CartItem, User,Cart
admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(CartItem)
admin.site.register(Cart)

# admin.site.register(Seller)


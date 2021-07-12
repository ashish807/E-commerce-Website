from django.contrib import admin
from .models import Cart, CartItem
# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display=('cart_id', 'date_added')

admin.site.register(Cart, CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    list_display=('product', 'cart', 'quantity', 'is_active')

admin.site.register(CartItem, CartItemAdmin)

# class BuyNowAdmin(admin.ModelAdmin):
#     list_display=('product', 'cart' ,'user' ,'quantity', 'is_active')

# admin.site.register(BuyNow, BuyNowAdmin)
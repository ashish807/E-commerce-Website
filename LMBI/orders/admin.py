from django.contrib import admin

from .models import Payment, Order, OrderProduct

# Register your models here.

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment','user','product', 'quantity','product_price', 'ordered')
    extra =0



class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'get_full_name', 'phone',  'is_ordered', 'created_at', 'checked_and_ready_for_shipping','delivery_guy_checked','order_recieved_by_client']
    list_editable =['checked_and_ready_for_shipping','delivery_guy_checked', 'order_recieved_by_client']
    list_filter=['is_ordered','checked_and_ready_for_shipping','delivery_guy_checked','order_recieved_by_client']
    search_fields =['order_number', 'first_name', 'phone', 'email']
    list_per_page  =20
    inlines =[OrderProductInline]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)

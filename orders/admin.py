from django.contrib import admin
from .models import (
    ShopCart,
    Order,
    OrderDetail,
)
# Register your models here.

class ShopCartAdmin(admin.ModelAdmin):
    list_display = ('user',  'quantity')


class DetailInline(admin.TabularInline):
    model = OrderDetail


class OrderAdmin(admin.ModelAdmin):
    list_display=('user', 'name', 'surname', 'city', 'phone', 'total', 'status')
    list_filter = ('status', 'create_at')
    readonly_fields = ('name', 'surname', 'address', 'city', 'phone', 'total', 'user')
    # inlnes =DetailInline


class OrderDetailAdmin(admin.ModelAdmin):
    list_display=('user', 'product', 'quantity', 'price', 'total', 'update_at')
    readonly_fields = ('product', 'quantity', 'price', 'total',)


admin.site.register(Order, OrderAdmin)
admin.site.register(ShopCart, ShopCartAdmin)
admin.site.register(OrderDetail, OrderDetailAdmin)
from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem


class OrderItemsInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemsInline, ]


admin.site.register(Order, OrderAdmin)

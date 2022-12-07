from django.contrib import admin
from .models import Order, OrderItem, OrderUpdate

# Register your models here.
class OrderFilter(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ["email", "id", "payment", "payment_completed"]
    list_filter = ["id"]


class OrderItemFilter(admin.ModelAdmin):
    search_fields = ("vendor",)
    list_display = ["vendor", "vendor_paid", "id"]
    list_filter = ["id", "vendor", "vendor_paid"]


class OrderUpdateFilter(admin.ModelAdmin):
    search_fields = ("id",)
    list_display = ["update_desc", "id"]
    list_filter = ["id"]


admin.site.register(Order, OrderFilter)
admin.site.register(OrderItem, OrderItemFilter)
admin.site.register(OrderUpdate, OrderUpdateFilter)

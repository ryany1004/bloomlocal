from django.contrib import admin

from bloom.order import models


class OrderItemInlineAdmin(admin.TabularInline):
    model = models.OrderItem
    extra = 1


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'shopper', 'total_price', 'status', 'payment_intent')
    list_filter = ('status',)
    search_fields = ('uuid', 'shopper__email', 'shopper__last_name', 'shopper__first_name', 'payment_intent')
    inlines = [OrderItemInlineAdmin]

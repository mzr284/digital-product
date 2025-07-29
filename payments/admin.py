from django.contrib import admin
from .models import Payment, Gateway

@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_enable']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'subscription', 'gateway', 'price', 'status']
    list_filter = ['status', 'gateway']
    search_fields = ['user__username']

from django.contrib import admin
from .models import Product, Customer, Order, OrderItem, ActivityLog, SupportTicket, SiteSetting

admin.site.site_header = "HOUSE OF NISSI NYAMEANI - Admin"
admin.site.site_title = "Nissi Admin"
admin.site.index_title = "Welcome, Madam Nissi 👑"

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_featured')
    list_filter = ('category',)
    search_fields = ('name',)
    list_editable = ('price', 'stock', 'is_featured')

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location', 'total_orders', 'total_spent', 'created_at')
    search_fields = ('user__username', 'phone')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total', 'status', 'payment_method', 'created_at')
    list_filter = ('status',)
    list_editable = ('status',)
    inlines = [OrderItemInline]

@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'details', 'created_at')
    list_filter = ('action',)

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'status', 'created_at')
    list_filter = ('status',)
    list_editable = ('status',)

admin.site.register(SiteSetting)
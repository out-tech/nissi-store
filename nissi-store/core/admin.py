from django.contrib import admin
from .models import Category, Product, CartItem, Order, OrderItem, SpecialOrder, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'description']
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available']
    search_fields = ['name']

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'full_name', 'phone', 'total_amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['full_name', 'phone']
    inlines = [OrderItemInline]

@admin.register(SpecialOrder)
class SpecialOrderAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'size', 'budget', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['name', 'phone']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'is_approved', 'created_at']
    list_filter = ['rating', 'is_approved']

admin.site.register(CartItem)
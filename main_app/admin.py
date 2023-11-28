from django.contrib import admin

from main_app.models import UserProfile, Product, Categories, Payment, Cart


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    model = UserProfile


admin.site.register(UserProfile, UserAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'details',
        'quantity',
        'price',
        'image',
        'category',
    ]
    search_fields = ['name']
    list_filter = ['category']
    list_per_page = 25


@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'added_at',
        'modified_at'
    ]
    search_fields = ['name']
    list_per_page = 25


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'quantity',
        'user',
        'payed_at'
    ]
    search_fields = ['product']
    list_filter = ['payed_at']
    list_per_page = 25


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = [
        'product',
        'user',
        'quantity',
        'is_ordered',
        'is_removed',
        'added_at',
        'modified_at',
    ]
    list_filter = ['is_ordered', 'is_removed', 'added_at', 'modified_at']
    search_fields = ['product']
    list_per_page = 25

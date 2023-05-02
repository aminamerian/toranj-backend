from django.contrib import admin
from .models import Category, Product, Shop, PriceChangeLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'is_leaf')
    list_filter = ('is_leaf',)
    raw_id_fields = ('parent',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('uid', 'category', 'name', 'price', 'features', 'is_available', 'shop', 'get_updated_at')
    list_filter = ('is_available',)
    raw_id_fields = ('category', 'shop',)

    def get_updated_at(self, obj):
        return obj.date_updated.strftime("%Y-%m-%d %H:%M:%S")

    get_updated_at.short_description = 'updated at'


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('name', 'domain')


@admin.register(PriceChangeLog)
class PriceChangeLogAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'is_available', 'date')

    def get_date(self, obj):
        return obj.date_updated.strftime("%Y-%m-%d %H:%M:%S")

    get_date.short_description = 'date'

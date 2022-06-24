from django.contrib import admin
from .models import Product, Category, Cart, Invoice, InvoiceItem, ImgsProduct

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'name', 'detail', 'enable', 'show_image']


class ProductImageAdmin(admin.StackedInline):
    model = ImgsProduct
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id', 'category', 'name',
                    'detail', 'price', 'enable', 'show_image']
    inlines = [ProductImageAdmin]


class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ['id', 'product', 'user', 'quantity', 'total']


class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    list_display = ['id', 'user', 'created', 'updated', 'total', 'status']


class InvoiceItemAdmin(admin.ModelAdmin):
    model = InvoiceItem
    list_display = ['product', 'invoice', 'created', 'quantity', 'total']


admin.site.register(ImgsProduct)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)

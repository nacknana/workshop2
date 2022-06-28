from django.contrib import admin
from .models import Contact, Product, Category, Cart, Invoice, InvoiceItem, ImgsProduct

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['id', 'name', 'detail', 'enable', 'show_image']
    list_editable = ['name', 'detail', 'enable']


class ProductImageAdmin(admin.StackedInline):
    model = ImgsProduct
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['id', 'category', 'name',
                    'detail', 'price', 'enable', 'show_image']
    list_editable = ['category', 'name', 'detail', 'price', 'enable']
    inlines = [ProductImageAdmin]


class CartAdmin(admin.ModelAdmin):

    model = Cart
    list_display = ['id', 'product', 'user', 'quantity', 'total']

    # def edit_quantity():


class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    list_display = ['id', 'user', 'created', 'updated', 'total', 'status']
    list_editable = ['status']


class InvoiceItemAdmin(admin.ModelAdmin):
    model = InvoiceItem
    list_display = ['product', 'invoice', 'created', 'quantity', 'total']


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ['first_name', 'detail', 'created', 'status']
    list_editable = ['status']


admin.site.register(ImgsProduct)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(InvoiceItem, InvoiceItemAdmin)
admin.site.register(Contact, ContactAdmin)

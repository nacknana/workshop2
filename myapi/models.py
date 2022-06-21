from django.db import models
from django.utils.html import format_html
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250)
    img = models.ImageField(upload_to='Categories', null=True, blank=True)
    detail = models.TextField(null=True, blank=True, max_length=255)
    enable = models.BooleanField(default=True)

    def show_image(self):
        if self.img:
            return format_html('<img src="' + self.img.url + '" height="100px">')
        return ''
    show_image.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Category'


class Product(models.Model):
    category = models.ForeignKey(Category, default=None,
                                 blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0)
    detail = models.TextField(null=True, blank=True, max_length=255)
    img = models.ImageField(upload_to='product')
    enable = models.BooleanField(default=True)

    def show_image(self):
        if self.img:
            return format_html('<img src="' + self.img.url + '" height="100px">')
        return ''
    show_image.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Product'


class ImgsProduct(models.Model):
    product = models.ForeignKey(Product, default=None, related_name='imgs_product',
                                blank=True, null=True, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='Product', null=True, blank=True)

    class Meta:
        verbose_name = 'img'
        verbose_name_plural = 'img'

    def __str__(self):
        return self.product.name


class Cart(models.Model):
    product = models.ForeignKey(
        Product, default=None, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Cart'


status_invoice_choice = (
    ('waiting', 'รอส่ง'),
    ('sened', 'ส่งแล้ว'),
    ('cancle', 'ยกเลิก'),
)


class Invoice(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total = models.IntegerField(default=0)
    status = models.CharField(
        max_length=20, choices=status_invoice_choice, default='waiting')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = 'Invoice'


class InvoiceItem(models.Model):
    product = models.ForeignKey(
        Product, default=None, blank=True, null=True, on_delete=models.CASCADE)
    invoice = models.ForeignKey(
        Invoice, default=None, blank=True, null=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def __str__(self):
        return self.invoice.user.username

    class Meta:
        verbose_name_plural = 'InvoiceItem'

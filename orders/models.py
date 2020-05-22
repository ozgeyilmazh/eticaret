from django.db import models
from django.contrib.auth.models import User

from products.models import Product
# Create your models here.


# Kullanıcı Bazlı Sepet Tutarı Hesaplıyor
class ShopCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
    )
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    @property
    def amount(self):
        return (self.quantity * self.product.salePrice)


# Sipariş ve Sipariş Sonrası Müşteri Bilgilendirme
class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preparing', 'Preparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=10)
    surname = models.CharField(max_length=10)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    total = models.FloatField()
    note = models.TextField(
        null=True,
        default="",
    )
    status = models.CharField(
        choices=STATUS,
        default='New',
        max_length=15,
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Sipariş Detay
class OrderDetail(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title
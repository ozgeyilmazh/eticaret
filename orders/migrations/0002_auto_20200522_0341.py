# Generated by Django 2.2 on 2020-05-22 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_auto_20200520_1731'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopcart',
            name='product',
        ),
        migrations.AddField(
            model_name='shopcart',
            name='product',
            field=models.ManyToManyField(blank=True, to='products.Product'),
        ),
    ]

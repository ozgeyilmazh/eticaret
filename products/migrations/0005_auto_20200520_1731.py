# Generated by Django 2.2.4 on 2020-05-20 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200520_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='type',
            field=models.CharField(choices=[('men', 'Erkek'), ('women', 'Kadın'), ('unisex', 'Unisex'), ('slider', 'Slider'), ('slider2', 'Slider2'), ('category', 'Kategory')], default='general', max_length=8),
        ),
    ]

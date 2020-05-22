from django.contrib import admin
from .models import Category, Product, Comment
# Register your models here.

from django import forms


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("title",)}
    list_display = (
        'pk',
        'title',
        'slug',
        'type',
        'status',
        'updated_at',
    )
    list_filter = ('status', 'type', )
    list_editable = (
        'status',
    )


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("title",)}
    list_display = (
        'pk',
        'title',
        'stock',
        'slug',
        'is_home',
        'status',
        'updated_at',
    )
    list_filter = ('status',  )
    list_editable = (
        'status',
        'title',
        'is_home',

    )


class CommentAdmin(admin.ModelAdmin):
    class Meta:
        model = Comment
    list_display = (
        'name',
        'productPost',
        'approved_comment',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment, CommentAdmin)
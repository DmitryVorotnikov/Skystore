from django.contrib import admin
from catalog.models import Product, Category, Article, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'price',
        'category',
        'is_published',
    )
    list_filter = ('category',)
    search_fields = ('name', 'description',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_published',)
    list_filter = ('is_published',)
    search_fields = ('title', 'content',)


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'version_number',
        'is_active',
    )
    list_filter = ('is_active',)
    search_fields = ('name', 'version_number',)

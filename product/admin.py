from django.contrib import admin

from .models import Category, Team, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'body', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('author', 'product', 'body')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(active=True)

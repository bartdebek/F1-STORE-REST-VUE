from django.contrib import admin

from .models import Category, Team, Product, Review


admin.site.register(Category)
admin.site.register(Team)
admin.site.register(Product)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'body', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('author', 'product', 'body')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(active=True)

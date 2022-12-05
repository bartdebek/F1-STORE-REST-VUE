from django.contrib import admin

from .models import Category, Team, Product, Review


admin.site.register(Category)
admin.site.register(Team)
admin.site.register(Product)
admin.site.register(Review)

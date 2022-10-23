from django.contrib import admin

from .models import Category, Team, Product


admin.site.register(Category)
admin.site.register(Team)
admin.site.register(Product)

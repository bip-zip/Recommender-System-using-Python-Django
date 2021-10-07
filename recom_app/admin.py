from django.contrib import admin
from .models import Category, Product, OrderItems,SearchHistory,Rating

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItems)
admin.site.register(SearchHistory)
admin.site.register(Rating)
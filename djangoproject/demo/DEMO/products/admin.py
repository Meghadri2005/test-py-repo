from django.contrib import admin

# Register your models here.
from .models import Product, Review, WishlistItem, ProductTracking
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(WishlistItem)
admin.site.register(ProductTracking)
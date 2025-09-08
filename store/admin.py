from django.contrib import admin
from .models import Category, Product, Order

# ثبت مدل‌ها برای ادمین
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Order)

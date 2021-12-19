from django.contrib import admin
from .models import Order, Customer, Product, Provider, ProductProvider, OrderDetail

# Register your models here.


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductProvider)
class ProductProviderAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    pass

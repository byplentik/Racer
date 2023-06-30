from django.contrib import admin

from . import models


@admin.register(models.Category)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.Motorcycle)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'category']


@admin.register(models.MainPart)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'motorcycle']
    prepopulated_fields = {'slug': ['name']}


@admin.register(models.Part)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'main_part', 'price', 'number']


@admin.register(models.Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ['user', 'completed']


@admin.register(models.CartItem)
class AdminCartItem(admin.ModelAdmin):
    list_display = ['part', 'cart', 'quantity']
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


@admin.register(models.Part)
class AdminCategory(admin.ModelAdmin):
    list_display = ['name', 'main_part', 'price', 'number']
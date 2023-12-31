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


class OrderedPartInline(admin.TabularInline):
    model = models.OrderedPart
    extra = 0
    readonly_fields = ('part', 'quantity')


@admin.register(models.CheckoutCart)
class CheckoutCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'created_at')
    inlines = (OrderedPartInline,)


admin.site.register(models.OrderedPart)

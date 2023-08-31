from django.db import models
from django.urls import reverse

from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Motorcycle(models.Model):
    name = models.CharField(max_length=255, verbose_name='Мото/Двигатели')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    slug = models.SlugField(max_length=300, verbose_name='URL', unique=True)
    excel_file = models.FileField(verbose_name='Excel файл', blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('motorcycle-detail', kwargs={'slug': self.slug})


class MainPart(models.Model):
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, verbose_name='Мото/Двигатель')
    name = models.CharField(max_length=255, verbose_name='Основная запчасть')
    image = models.ImageField(upload_to='mainpart/', blank=True)

    def __str__(self):
        return self.name


class Part(models.Model):
    main_part = models.ForeignKey(MainPart, on_delete=models.CASCADE, verbose_name='Основная запчасть')
    number = models.IntegerField(verbose_name='№')
    code = models.CharField(max_length=150, verbose_name='Уникальный код', blank=True)
    name = models.CharField(max_length=300, verbose_name='Наименование')
    price = models.IntegerField(default=0, verbose_name='Цена')

    class Meta:
        ordering = ['number']

    def __str__(self):
        return self.name


class CheckoutCart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'{self.user}'


class OrderedPart(models.Model):
    cart = models.ForeignKey(CheckoutCart, on_delete=models.CASCADE, related_name='ordered_parts', verbose_name='Оформленный заказ')
    part = models.ForeignKey('Part', on_delete=models.CASCADE, verbose_name='Запчасть')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    def __str__(self):
        return f'{self.cart}'

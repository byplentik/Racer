from django.db import models
from django.urls import reverse


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

    def __str__(self):
        return self.name


class MainPart(models.Model):
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, verbose_name='Мото/Двигатель')
    name = models.CharField(max_length=255, verbose_name='Основная запчасть')
    slug = models.SlugField(max_length=300, verbose_name='URL', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('part-detail', kwargs={'slug': self.slug})


class Part(models.Model):
    main_part = models.ForeignKey(MainPart, on_delete=models.CASCADE, verbose_name='Основная запчасть')
    number = models.IntegerField(verbose_name='№')
    name = models.CharField(max_length=300, verbose_name='Наименование')
    price = models.IntegerField(default=0, verbose_name='Цена')

    def __str__(self):
        return self.name

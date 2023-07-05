import uuid

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


class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('cart-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
        cartitems = self.cartitems.all()
        total = sum([item.part.price * item.quantity for item in cartitems])
        return total

    @property
    def get_num_of_items(self):
        cartitems = self.cartitems.all()
        quantity = sum([item.quantity for item in cartitems])
        return quantity


class CartItem(models.Model):
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='items')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.part.name


    # @property
    # def price(self):
    # """Для подсчета общей цены вместе с количеством на единицу товара"""
    #     new_price = self.part.price * self.quantity
    #     return new_price

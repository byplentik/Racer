from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.utils.html import format_html
from django_mail_admin.models import OutgoingEmail, EmailTemplate

from users.models import DeliveryAddressModel


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
    excel_file = models.FileField(verbose_name='Excel файл для загрузки данных', blank=True, upload_to='excel_moto/')

    class Meta:
        verbose_name = 'Мотоцикл | Двигатель'
        verbose_name_plural = 'Мотоциклы | Двигатели'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('motorcycle-detail', kwargs={'slug': self.slug})


class Engine(models.Model):
    url = models.URLField(verbose_name='URL двигателя')
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, verbose_name='Мото/Двигатель', blank=True, null=True, related_name='engines')

    class Meta:
        verbose_name = 'Ссылка на двигатели'
        verbose_name_plural = 'Ссылка на двигатели'

    def __str__(self):
        return f'{self.url}'


class MainPart(models.Model):
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE, verbose_name='Мото/Двигатель')
    name = models.CharField(max_length=255, verbose_name='Основная запчасть')
    image = models.ImageField(upload_to='mainpart/', blank=True)
    ordering = models.IntegerField(db_index=True, verbose_name='Сортировка')

    class Meta:
        verbose_name = 'Основная запчасть'
        verbose_name_plural = 'Основные запчасти'
        ordering = ['ordering']

    def __str__(self):
        return self.name


class Part(models.Model):
    main_part = models.ForeignKey(MainPart, on_delete=models.CASCADE, verbose_name='Основная запчасть', blank=True, null=True)
    number = models.CharField(verbose_name='№', max_length=10)
    code = models.CharField(max_length=150, verbose_name='Уникальный код', blank=True)
    name = models.CharField(max_length=300, verbose_name='Наименование')
    price = models.IntegerField(default=0, verbose_name='Цена')

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'

    def __str__(self):
        return self.name


class NotePartModel(models.Model):
    note = models.CharField(max_length=255, verbose_name='Примечание')
    part = models.ForeignKey('Part', on_delete=models.CASCADE, verbose_name='Запчасть', related_name='notes')


class OrderStatus(models.TextChoices):
    WAITING = 'Waiting', 'Ожидание'
    ACCEPTED = 'Accepted', 'Заказ принят'
    SHIPPED = 'Shipped', 'Отправлено'
    CANCELED = 'Canceled', 'Отменен'


class CheckoutCart(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')
    delivery_address = models.ForeignKey('SpecifiedDeliveryAddressModel', on_delete=models.SET_NULL, verbose_name='Адрес доставки', blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий к заказу')
    order_status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.WAITING,
        verbose_name='Статус заказа'
    )

    class Meta:
        verbose_name = 'Оформленный заказ'
        verbose_name_plural = 'Оформленные заказы'

    def __str__(self):
        return f'Номер заказа: {self.pk}'

    @admin.display(description='Номер заказа', ordering='pk')
    def id_as_order_number(self):
        return int(self.pk)

    @admin.display(description='Заказчик')
    def client(self):
        return f'{self.delivery_address.full_name}'


class OrderedPart(models.Model):
    cart = models.ForeignKey(CheckoutCart, on_delete=models.CASCADE, related_name='ordered_parts', verbose_name='Оформленный заказ')
    part = models.ForeignKey('Part', on_delete=models.CASCADE, verbose_name='Запчасть')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Оформленная запчасть'
        verbose_name_plural = 'Оформленные запчасти'

    def __str__(self):
        return f'{self.cart}'


class ExcelFileCatalog(models.Model):
    excel_file = models.FileField(verbose_name='Каталог',
                                  help_text='Загрузите Excel файл для обновления каталога запчастей', upload_to='files_main_price/')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Excel файлы для загрузки цен'
        verbose_name_plural = 'Excel файлы для загрузки цен'


class AdditionalItemToCheckoutCart(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    price = models.IntegerField(verbose_name='Цена')
    cart = models.ForeignKey(CheckoutCart, on_delete=models.SET_NULL, related_name='additional_item', blank=True, null=True)

    class Meta:
        verbose_name = 'Добавить пустое поле'
        verbose_name_plural = 'Добавить пустое поле'

    def __str__(self):
        return f'{self.name} - {self.price}'


class CommentAdministratorForCheckoutCart(models.Model):
    comment = models.TextField(verbose_name='Комментарий')
    cart = models.ForeignKey(CheckoutCart, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        verbose_name = 'Комментарий администратора'
        verbose_name_plural = 'Комментарий администратора'


class DeliveryMethod(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    price = models.IntegerField(verbose_name='Цена')
    cart = models.OneToOneField(CheckoutCart, on_delete=models.SET_NULL, related_name='delivery_method', blank=True, null=True)
    total_price_with_delivery = models.IntegerField(verbose_name='Цена', blank=True, null=True)

    class Meta:
        verbose_name = 'Добавить способ доставки'


class SpecifiedDeliveryAddressModel(models.Model):
    COUNTRIES_CHOICES = [
        ("RUSSIA", "Россия"),
        ("BELARUS", "Беларусь"),
        ("KAZAKHSTAN", "Казахстан"),
    ]

    full_name = models.CharField(verbose_name='ФИО', max_length=455)
    phone_number = models.IntegerField(verbose_name='Номер телефона')
    postal_code = models.IntegerField(verbose_name='Почтовый код')
    country = models.CharField(verbose_name='Страна', max_length=20, choices=COUNTRIES_CHOICES, blank=True, null=True)
    delivery_address = models.CharField(verbose_name='Адрес доставки', max_length=455)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Пользователь')


class SendEmailAtCheckoutCartModel(models.Model):
    checkout_order = models.OneToOneField(CheckoutCart, on_delete=models.CASCADE, related_name='send_email_cart_order')
    outgoing_email = models.OneToOneField(OutgoingEmail, on_delete=models.CASCADE, related_name='send_email_cart_outgoing_email', blank=True, null=True)
    template = models.ForeignKey(EmailTemplate, on_delete=models.CASCADE, blank=True, null=True)
    from_email = models.EmailField(max_length=255, blank=True, null=True)
    to_email = models.EmailField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f'{self.pk}'

    class Meta:
        verbose_name = 'Отправить письмо пользователю'
        verbose_name_plural = 'Отправить письмо пользователю'
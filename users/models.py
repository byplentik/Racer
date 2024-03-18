from django.db import models
from django.urls import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)

from autoslug import AutoSlugField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Пользователь должен указать email адрес')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(email, username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    username = models.CharField(verbose_name='Имя пользователя', max_length=255)
    slug = AutoSlugField(populate_from='username', unique=True, always_update=True)

    old_user_id = models.IntegerField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(
        ('статус персонала'),
        default=False,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'slug': self.slug})


class DeliveryAddressModel(models.Model):
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
    name_address = models.CharField(verbose_name='Сохранить как', max_length=455, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return f'{self.user} - {self.name_address}'

    class Meta:
        verbose_name = 'Адресная книга'
        verbose_name_plural = 'Адресная книга пользователей'

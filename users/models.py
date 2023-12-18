from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, last_name, password=None):
        if not email:
            raise ValueError('Пользователь должен указать email адрес')

        user = self.model(
            name=name,
            last_name=last_name,
            email=email
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, last_name, password=None):
        user = self.create_user(email, name=name, last_name=last_name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(verbose_name='Номер телефона', unique=True, max_length=20, blank=True)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)
    name = models.CharField(verbose_name='Имя', max_length=255, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255, blank=True)
    delivery_address = models.TextField(
        verbose_name='Полный адрес доставки',
        help_text='Введите полный адрес доставки (Страна, Город, Улица, Дом)',
        null=True, blank=True
        )
    delivery_index = models.IntegerField(
        verbose_name='Индекс',
        help_text='Это индекс почтового отделения, куда будет доставлена посылка из вашего заказа',
        null=True, blank=True
    )

    is_staff = models.BooleanField(
        ('статус персонала'),
        default=False,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'last_name']

    def __str__(self):
        return f'{self.phone_number}'

    @property
    def get_full_name(self):
        return f'{self.name} {self.last_name}'

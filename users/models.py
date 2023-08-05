from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)


class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, name, last_name, password=None):
        if not phone_number:
            raise ValueError('Пользователь должен указать номер телефона')

        user = self.model(
            name=name,
            last_name=last_name,
            phone_number=phone_number
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, name, last_name, password=None):
        user = self.create_user(phone_number, name=name, last_name=last_name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(verbose_name='Номер телефона', unique=True, max_length=20)
    email = models.EmailField(verbose_name='Email', max_length=255, blank=True)
    name = models.CharField(verbose_name='Имя', max_length=255, blank=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=255, blank=True)
    is_staff = models.BooleanField(
        ('статус персонала'),
        default=False,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name', 'last_name']

    def __str__(self):
        return f'{self.phone_number}'

    @property
    def get_full_name(self):
        return f'{self.name} {self.last_name}'

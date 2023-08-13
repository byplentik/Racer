from django import forms
from django.contrib.auth import get_user_model

from hcaptcha.fields import hCaptchaField


class CheckoutFromCartForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['name', 'last_name', 'email', 'delivery_address', 'delivery_index']


class CheckoutFromCartFormNotAuth(forms.Form):
    phone_number = forms.CharField(label='Номер телефона', help_text='На него будет выслан код подтверждения для завершения регистрации')
    email = forms.EmailField(label='Email', max_length=255)
    name = forms.CharField(label='Имя', max_length=255)
    last_name = forms.CharField(label='Фамилия', max_length=255)
    delivery_address = forms.CharField(
        label='Полный адрес доставки',
        help_text='Введите полный адрес доставки (Страна, Город, Улица, Дом)',
    )
    delivery_index = forms.IntegerField(
        label='Индекс',
        help_text='Это индекс почтового отделения, куда будет доставлена посылка из вашего заказа',
    )
    hcaptcha = hCaptchaField()


class VerifyCodeFormAndCreateOrder(forms.Form):
    code = forms.CharField(max_length=6, label='Проверочный код')
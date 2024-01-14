from django import forms
from django.contrib.auth import get_user_model

from users.models import DeliveryAddressModel


class CheckoutFromCartForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-custom-form', 'placeholder': 'Фамилия Имя Отчество'}), max_length=455, required=True)
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input-custom-form', 'placeholder': '79008008080'}), required=True)
    postal_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input-custom-form', 'placeholder': '600900'}), required=True)
    country_and_city = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-custom-form', 'placeholder': 'Россия, Москва'}), max_length=455, required=True)
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-custom-form', 'placeholder': 'Ул Пушкина 40'}), max_length=455, required=True)
    comment = forms.CharField(widget=forms.TextInput(attrs={'class': 'input-custom-form', 'placeholder': 'Например: цвет, способ доставки, дополнение или вопрос.'}), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', False)
        super(CheckoutFromCartForm, self).__init__(*args, **kwargs)

        # Если не авторизован
        if not user.is_authenticated:
            self.fields['email'] = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'input-custom-form', 'placeholder': 'Например: Email.com'}))

        if user.is_authenticated and DeliveryAddressModel.objects.filter(user=user).exists():
            self.fields['name_address'] = forms.ModelChoiceField(
                queryset=DeliveryAddressModel.objects.none(),
                empty_label=None,
                widget=forms.Select(attrs={'class': 'input-custom-form'}),
                required=False,
            )
            self.fields['name_address'].label = 'Выбрать адрес'

        # Меняю значение label у полей
        self.fields['full_name'].label = 'ФИО'
        self.fields['phone_number'].label = 'Номер телефона'
        self.fields['postal_code'].label = 'Почтовый код'
        self.fields['country_and_city'].label = 'Страна и город'
        self.fields['delivery_address'].label = 'Адрес доставки'
        self.fields['comment'].label = 'Комментарий к заказу'

    class Meta:
        fields = ['full_name', 'phone_number', 'postal_code', 'country_and_city', 'delivery_address']




from django import forms
from django.contrib.auth import get_user_model
from django_mail_admin.models import EmailTemplate

from users.models import DeliveryAddressModel
from basket.models import Motorcycle


class CheckoutFromCartForm(forms.Form):
    full_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия Имя Отчество'}), max_length=455, required=True)
    phone_number = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '79008008080'}), required=True)
    postal_code = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '600900'}), required=True)
    country = forms.ChoiceField(
        choices=DeliveryAddressModel.COUNTRIES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    delivery_address = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Московская область, Г. Одинцово, ул Пушкина 40'}), max_length=455, required=True)
    comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Например: цвет, способ доставки, дополнение или вопрос.'}), required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', False)
        super(CheckoutFromCartForm, self).__init__(*args, **kwargs)

        # Если не авторизован
        if not user.is_authenticated:
            self.fields['email'] = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Например: example@email.com'}))

        if user.is_authenticated and DeliveryAddressModel.objects.filter(user=user).exists():
            self.fields['name_address'] = forms.ModelChoiceField(
                queryset=DeliveryAddressModel.objects.none(),
                widget=forms.Select(attrs={'class': 'form-control'}),
                required=False,
            )
            self.fields['name_address'].label = 'Выбрать адрес'

        # Меняю значение label у полей
        self.fields['full_name'].label = 'ФИО'
        self.fields['phone_number'].label = 'Номер телефона'
        self.fields['postal_code'].label = 'Почтовый код (индекс)'
        self.fields['country'].label = 'Страна'
        self.fields['delivery_address'].label = 'Адрес доставки'
        self.fields['comment'].label = 'Комментарий к заказу'

    class Meta:
        fields = ['full_name', 'phone_number', 'postal_code', 'country_and_city', 'delivery_address']


class MotorcycleAdminForm(forms.ModelForm):
    imgs_for_mainparts = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Загрузите изображения для запчастей', required=False)

    class Meta:
        model = Motorcycle
        fields = '__all__'


class PartSearchForm(forms.Form):
    text = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Поиск по каталогу'}),
    )


class SendInfoEmailForm(forms.Form):
    to_email = forms.EmailField()
    template_email = forms.ModelChoiceField(queryset=EmailTemplate.objects.all(), empty_label=None)
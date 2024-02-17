from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField, PasswordResetForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

from .models import CustomUser, DeliveryAddressModel


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают!")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Ваш Email адрес'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтвердите пароль'

        self.fields['email'].widget.attrs['placeholder'] = 'example@email.com'
        self.fields['password1'].widget.attrs['placeholder'] = 'Придумайте пароль'
        self.fields['password2'].widget.attrs['placeholder'] = 'Повторите пароль'

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'is_staff']


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Ваш Email адрес'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            user_login = authenticate(email=email, password=password)
            cleaned_data.update({'user_login': user_login})

            if not user_login or not user_login.is_active:
                raise forms.ValidationError("Неверный email или пароль")

        return cleaned_data


class EditUserForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}), required=True)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Текущий пароль'}), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Ваш Email адрес'
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password'].label = 'Пароль'


class UserChangePasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Текущий пароль'
        self.fields['new_password1'].label = 'Новый пароль'
        self.fields['new_password2'].label = 'Подтвердите новый пароль'

        placeholders = {
            'old_password': 'Введите ваш текущий пароль',
            'new_password1': 'Новый пароль',
            'new_password2': 'Повторите новый пароль',
        }

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name in placeholders:
                field.widget.attrs['placeholder'] = placeholders[field_name]


class DeliveryAddressAddForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddressModel
        fields = ['full_name', 'phone_number', 'postal_code', 'country', 'delivery_address', 'name_address']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия Имя Отчество'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '79008008080'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '600900'}),
            'country': forms.Select(attrs={'class': 'form-control'}),
            'delivery_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ул Пушкина 40'}),
            'name_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Дом, работа'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        for field_name in self.fields:
            self.fields[field_name].required = True

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user

        if commit:
            instance.save()
        return instance


class PasswordResetCustomForm(PasswordResetForm):
    email = forms.EmailField(
        label='Email адрес для сброса пароля',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@email.com'}),
    )

    class Meta:
        fields = ['email']